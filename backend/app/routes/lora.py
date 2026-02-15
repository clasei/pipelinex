"""
Training routes for real LoRA fine-tuning
"""
import asyncio
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from app.services.lora_trainer import LoRATrainer, LoRATrainingConfig

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/lora", tags=["lora"])

# Global trainer instance
trainer: Optional[LoRATrainer] = None
BACKEND_DIR = Path(__file__).parent.parent.parent


def get_lora_trainer():
    """Get or create LoRA trainer instance"""
    global trainer
    if trainer is None:
        trainer = LoRATrainer(
            model_name="mistralai/Mistral-7B-v0.1",
            output_dir="./lora_models",
            use_4bit=True,  # Use 4-bit quantization to save memory
        )
    return trainer


class LoRATrainingRequest(BaseModel):
    data_path: str
    lora_r: int = 8
    lora_alpha: int = 16
    lora_dropout: float = 0.05
    learning_rate: float = 2e-4
    batch_size: int = 4
    epochs: int = 3
    max_length: int = 512


@router.post("/train/start")
async def start_lora_training(request: LoRATrainingRequest):
    """Start real LoRA fine-tuning"""

    trainer = get_lora_trainer()

    if trainer.is_training:
        return {"error": "training already in progress"}

    try:
        # Resolve data path
        data_path = Path(request.data_path)
        if not data_path.is_absolute():
            data_path = BACKEND_DIR / request.data_path
            if not data_path.exists():
                data_path = BACKEND_DIR / "training_data.jsonl"

        if not data_path.exists():
            raise HTTPException(status_code=404, detail=f"Training data not found: {data_path}")

        logger.info(f"📂 Training data: {data_path}")

        # Count examples
        with open(data_path, 'r') as f:
            num_examples = sum(1 for line in f if line.strip())

        logger.info(f"📊 {num_examples} training examples")

        # Create LoRA config
        config = LoRATrainingConfig(
            lora_r=request.lora_r,
            lora_alpha=request.lora_alpha,
            lora_dropout=request.lora_dropout,
            learning_rate=request.learning_rate,
            batch_size=request.batch_size,
            epochs=request.epochs,
            max_length=request.max_length,
        )

        # Start training in background
        async def train_task():
            try:
                model_path = await trainer.train(str(data_path), config)
                logger.info(f"✅ Training complete! Model saved to: {model_path}")
            except Exception as e:
                logger.error(f"❌ Training failed: {e}")
                trainer.is_training = False

        asyncio.create_task(train_task())

        return {
            "status": "training started",
            "config": {
                "lora_r": config.lora_r,
                "lora_alpha": config.lora_alpha,
                "learning_rate": config.learning_rate,
                "batch_size": config.batch_size,
                "epochs": config.epochs,
            },
            "data_path": str(data_path),
            "num_examples": num_examples,
            "note": "This is REAL LoRA fine-tuning - model weights will be updated!"
        }

    except Exception as e:
        logger.error(f"Failed to start training: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/train/status")
async def get_training_status():
    """Get current LoRA training status"""
    trainer = get_lora_trainer()
    return trainer.get_status()


@router.post("/train/stop")
async def stop_training():
    """Stop LoRA training (not implemented yet)"""
    return {"status": "stop not yet implemented for LoRA training"}


@router.post("/export/ollama")
async def export_to_ollama(model_path: str, ollama_name: str = "pipelinex-trained"):
    """
    Export trained LoRA model to Ollama

    This will:
    1. Merge LoRA adapters with base model
    2. Export to GGUF format
    3. Create Ollama model
    """
    try:
        trainer = get_lora_trainer()

        logger.info(f"📦 Exporting {model_path} to Ollama as {ollama_name}...")

        # Merge LoRA adapters
        merged_path = trainer.merge_and_export(
            adapter_path=model_path,
            output_path="./merged_models/final"
        )

        # TODO: Convert to GGUF and import to Ollama
        # This requires additional tools (llama.cpp)

        return {
            "status": "export started",
            "merged_model_path": merged_path,
            "note": "Full Ollama export requires llama.cpp conversion - coming soon!"
        }

    except Exception as e:
        logger.error(f"Export failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

