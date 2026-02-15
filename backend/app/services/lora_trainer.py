"""
Real LoRA Fine-tuning Trainer for Local LLMs
Uses PEFT (Parameter-Efficient Fine-Tuning) with LoRA
Optimized for Mac M3 (MPS) and CUDA
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
import asyncio

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType, PeftModel
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class LoRATrainingConfig:
    # LoRA-specific parameters
    lora_r: int = 8  # LoRA rank
    lora_alpha: int = 16  # LoRA alpha
    lora_dropout: float = 0.05
    target_modules: List[str] = None  # Will be set based on model

    # Training parameters
    learning_rate: float = 2e-4
    batch_size: int = 4
    epochs: int = 3
    max_length: int = 512
    warmup_steps: int = 10

    # Model parameters
    temperature: float = 0.7
    top_p: float = 0.95

    def __post_init__(self):
        if self.target_modules is None:
            # Default target modules for Mistral/Llama style models
            self.target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]


class LoRATrainer:
    """Professional LoRA trainer for local LLM fine-tuning"""

    def __init__(
        self,
        model_name: str = "mistralai/Mistral-7B-v0.1",
        output_dir: str = "./lora_models",
        use_4bit: bool = True,  # Use 4-bit quantization to save memory
    ):
        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.use_4bit = use_4bit

        # Detect device
        if torch.cuda.is_available():
            self.device = "cuda"
            logger.info("🚀 Using CUDA GPU")
        elif torch.backends.mps.is_available():
            self.device = "mps"
            logger.info("🍎 Using Apple Silicon MPS")
        else:
            self.device = "cpu"
            logger.info("💻 Using CPU (will be slow!)")

        self.model = None
        self.tokenizer = None
        self.is_training = False
        self.current_epoch = 0
        self.current_step = 0
        self.current_loss = 0.0
        self.total_steps = 0

        logger.info(f"✅ LoRA Trainer initialized: {model_name}")

    def load_model_and_tokenizer(self):
        """Load base model and tokenizer with optional quantization"""
        logger.info(f"📥 Loading model: {self.model_name}")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "right"

        # Quantization config for memory efficiency
        if self.use_4bit:
            from transformers import BitsAndBytesConfig

            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            )

            # Load model with quantization
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=quantization_config,
                device_map="auto",
                trust_remote_code=True,
            )
        else:
            # Load model without quantization
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
            )

        logger.info("✅ Model and tokenizer loaded")

    def prepare_lora_model(self, config: LoRATrainingConfig):
        """Prepare model with LoRA adapters"""
        logger.info("🔧 Preparing LoRA configuration...")

        lora_config = LoraConfig(
            r=config.lora_r,
            lora_alpha=config.lora_alpha,
            target_modules=config.target_modules,
            lora_dropout=config.lora_dropout,
            bias="none",
            task_type=TaskType.CAUSAL_LM,
        )

        # Add LoRA adapters to model
        self.model = get_peft_model(self.model, lora_config)

        # Print trainable parameters
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        all_params = sum(p.numel() for p in self.model.parameters())
        trainable_percent = 100 * trainable_params / all_params

        logger.info(f"🎯 Trainable parameters: {trainable_params:,} ({trainable_percent:.2f}%)")
        logger.info(f"📊 Total parameters: {all_params:,}")
        logger.info("✅ LoRA adapters added")

    def load_training_data(self, data_path: str, config: LoRATrainingConfig) -> Dataset:
        """Load and prepare training data from JSONL"""
        logger.info(f"📂 Loading training data: {data_path}")

        data = []
        with open(data_path, 'r') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))

        logger.info(f"✅ Loaded {len(data)} training examples")

        # Format conversations for training
        def format_prompt(example):
            prompt = example.get("prompt", "")
            completion = example.get("completion", "")

            # Format as conversation
            text = f"<s>[INST] {prompt} [/INST] {completion}</s>"
            return {"text": text}

        # Create dataset
        formatted_data = [format_prompt(ex) for ex in data]
        dataset = Dataset.from_list(formatted_data)

        # Tokenize
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                max_length=config.max_length,
                padding="max_length",
            )

        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset.column_names,
        )

        logger.info("✅ Data prepared and tokenized")
        return tokenized_dataset

    async def train(
        self,
        data_path: str,
        config: LoRATrainingConfig,
        progress_callback=None,
    ):
        """Run LoRA fine-tuning"""
        self.is_training = True

        try:
            # Load model if not already loaded
            if self.model is None:
                self.load_model_and_tokenizer()

            # Prepare LoRA
            self.prepare_lora_model(config)

            # Load and prepare data
            train_dataset = self.load_training_data(data_path, config)

            # Calculate total steps
            self.total_steps = (len(train_dataset) // config.batch_size) * config.epochs

            # Training arguments
            training_args = TrainingArguments(
                output_dir=str(self.output_dir / "checkpoints"),
                num_train_epochs=config.epochs,
                per_device_train_batch_size=config.batch_size,
                learning_rate=config.learning_rate,
                warmup_steps=config.warmup_steps,
                logging_steps=1,
                save_strategy="epoch",
                fp16=self.device != "cpu",
                optim="adamw_torch",
                gradient_accumulation_steps=1,
                report_to=[],  # Disable wandb for now
            )

            # Data collator
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=False,
            )

            # Custom callback for progress tracking
            from transformers import TrainerCallback

            class ProgressCallback(TrainerCallback):
                def __init__(self, trainer_instance, callback_func):
                    self.trainer_instance = trainer_instance
                    self.callback_func = callback_func

                def on_log(self, args, state, control, logs=None, **kwargs):
                    if logs:
                        self.trainer_instance.current_step = state.global_step
                        self.trainer_instance.current_epoch = int(state.epoch) if state.epoch else 0
                        self.trainer_instance.current_loss = logs.get("loss", 0.0)

                        logger.info(
                            f"📈 Epoch {self.trainer_instance.current_epoch}/{config.epochs} | "
                            f"Step {self.trainer_instance.current_step}/{self.trainer_instance.total_steps} | "
                            f"Loss: {self.trainer_instance.current_loss:.4f}"
                        )

            # Create trainer
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=train_dataset,
                data_collator=data_collator,
                callbacks=[ProgressCallback(self, progress_callback)],
            )

            logger.info("🚀 Starting LoRA fine-tuning...")

            # Train!
            trainer.train()

            logger.info("✅ Training complete!")

            # Save final model
            final_model_path = self.output_dir / "final_model"
            self.model.save_pretrained(final_model_path)
            self.tokenizer.save_pretrained(final_model_path)

            logger.info(f"💾 Model saved to: {final_model_path}")

            # Save training config
            config_path = final_model_path / "training_config.json"
            with open(config_path, 'w') as f:
                json.dump(asdict(config), f, indent=2)

            return str(final_model_path)

        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            raise

        finally:
            self.is_training = False

    def merge_and_export(self, adapter_path: str, output_path: str):
        """Merge LoRA adapters with base model and export"""
        logger.info("🔄 Merging LoRA adapters with base model...")

        # Load base model
        base_model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        # Load and merge LoRA adapters
        model = PeftModel.from_pretrained(base_model, adapter_path)
        merged_model = model.merge_and_unload()

        # Save merged model
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        merged_model.save_pretrained(output_path)
        self.tokenizer.save_pretrained(output_path)

        logger.info(f"✅ Merged model saved to: {output_path}")
        return str(output_path)

    def get_status(self) -> Dict[str, Any]:
        """Get current training status"""
        return {
            "is_training": self.is_training,
            "metrics": {
                "epoch": self.current_epoch,
                "step": self.current_step,
                "loss": self.current_loss,
                "total_steps": self.total_steps,
            },
            "model": self.model_name,
            "device": self.device,
        }

