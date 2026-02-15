import asyncio
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
    BitsAndBytesConfig
)
from threading import Thread

logger = logging.getLogger(__name__)


@dataclass
class TrainingConfig:
    model_name: str = "mistralai/Mistral-7B-Instruct-v0.1"
    learning_rate: float = 5e-5
    batch_size: int = 4
    epochs: int = 3
    max_steps: Optional[int] = None
    temperature: float = 0.7
    top_p: float = 0.95


@dataclass
class TrainingMetrics:
    epoch: int
    step: int
    loss: float
    throughput: float  # tokens/sec
    total_loss: float
    total_tokens: int


class LMTrainer:
    """Local LLM trainer for Mac M3"""

    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.1"):
        self.model_name = model_name
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        logger.info(f"using device: {self.device}")

        self.model = None
        self.tokenizer = None
        self.is_training = False
        self.is_paused = False

        # metrics tracking
        self.current_epoch = 0
        self.current_step = 0
        self.current_loss = 0.0
        self.total_loss = 0.0
        self.total_tokens = 0

    def load_model(self):
        """Load model and tokenizer with 8-bit quantization for mac"""
        logger.info(f"loading {self.model_name}")

        # 8-bit quantization config
        bnb_config = BitsAndBytesConfig(
            load_in_8bit=True,
            bnb_8bit_compute_dtype=torch.float16,
            bnb_8bit_use_double_quant=False,
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            device_map="mps" if self.device == "mps" else None,
            trust_remote_code=True,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        logger.info(f"model loaded: {self.model.config}")

    def load_data(self, data_path: str) -> list:
        """Load jsonl training data"""
        data = []
        path = Path(data_path)

        if not path.exists():
            logger.warning(f"data file not found: {data_path}")
            return data

        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))

        logger.info(f"loaded {len(data)} training examples")
        return data

    async def train(
        self,
        data_path: str,
        config: TrainingConfig,
        metrics_callback = None
    ):
        """Start training loop with real-time metrics streaming"""
        self.is_training = True
        self.is_paused = False

        # load data
        training_data = self.load_data(data_path)
        if not training_data:
            logger.error("no training data loaded")
            return

        # load model if not already loaded
        if self.model is None:
            self.load_model()

        logger.info("starting training...")

        try:
            for epoch in range(config.epochs):
                if not self.is_training:
                    break

                # wait if paused
                while self.is_paused and self.is_training:
                    await asyncio.sleep(0.1)

                self.current_epoch = epoch
                epoch_loss = 0.0

                for step, example in enumerate(training_data):
                    if not self.is_training:
                        break

                    # wait if paused
                    while self.is_paused and self.is_training:
                        await asyncio.sleep(0.1)

                    self.current_step = step

                    # prepare batch
                    prompt = example.get("prompt", "")
                    completion = example.get("completion", "")
                    full_text = f"{prompt}{completion}"

                    # tokenize
                    inputs = self.tokenizer(
                        full_text,
                        return_tensors="pt",
                        max_length=512,
                        truncation=True,
                    )

                    # move to device
                    inputs = {k: v.to(self.device) for k, v in inputs.items()}

                    # forward pass
                    outputs = self.model(**inputs, labels=inputs["input_ids"])
                    loss = outputs.loss

                    self.current_loss = float(loss.item())
                    epoch_loss += self.current_loss
                    self.total_loss += self.current_loss

                    num_tokens = inputs["input_ids"].shape[1]
                    self.total_tokens += num_tokens

                    # calculate throughput (tokens/sec)
                    throughput = num_tokens / 1.0  # simplified, 1 sec per batch

                    # emit metrics
                    metrics = TrainingMetrics(
                        epoch=epoch,
                        step=step,
                        loss=self.current_loss,
                        throughput=throughput,
                        total_loss=self.total_loss,
                        total_tokens=self.total_tokens
                    )

                    if metrics_callback:
                        await metrics_callback(metrics)

                    # log every 10 steps
                    if step % 10 == 0:
                        logger.info(
                            f"epoch {epoch} | step {step} | loss {self.current_loss:.4f}"
                        )

                    # yield control
                    await asyncio.sleep(0)

                avg_epoch_loss = epoch_loss / len(training_data)
                logger.info(f"epoch {epoch} complete | avg loss {avg_epoch_loss:.4f}")

        except Exception as e:
            logger.error(f"training error: {e}")
            self.is_training = False
            raise

        finally:
            self.is_training = False

    def pause(self):
        """Pause training"""
        self.is_paused = True
        logger.info("training paused")

    def resume(self):
        """Resume training"""
        self.is_paused = False
        logger.info("training resumed")

    def stop(self):
        """Stop training"""
        self.is_training = False
        self.is_paused = False
        logger.info("training stopped")

    def save_checkpoint(self, path: str):
        """Save model checkpoint"""
        if self.model is None:
            logger.warning("no model to save")
            return

        Path(path).mkdir(parents=True, exist_ok=True)
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        logger.info(f"checkpoint saved to {path}")

    def get_status(self) -> Dict[str, Any]:
        """Get current training status"""
        return {
            "is_training": self.is_training,
            "is_paused": self.is_paused,
            "epoch": self.current_epoch,
            "step": self.current_step,
            "loss": self.current_loss,
            "total_loss": self.total_loss,
            "total_tokens": self.total_tokens,
            "device": self.device,
        }

