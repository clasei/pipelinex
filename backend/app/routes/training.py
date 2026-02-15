import asyncio
import json
import os
from pathlib import Path
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Optional
from app.services.universal_trainer import UniversalLMTrainer, TrainingConfig
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/training", tags=["training"])

# global trainer instance - will be initialized on first use
trainer: Optional[UniversalLMTrainer] = None

# get absolute path to backend directory
BACKEND_DIR = Path(__file__).parent.parent.parent


def get_trainer():
    """Get or create trainer instance"""
    global trainer
    if trainer is None:
        trainer = UniversalLMTrainer(llm_source="ollama", model_name="mistral")
    return trainer


class HyperParameters(BaseModel):
    learning_rate: float = 5e-5
    batch_size: int = 4
    epochs: int = 3
    temperature: float = 0.7
    top_p: float = 0.95


class TrainingRequest(BaseModel):
    data_path: str
    params: HyperParameters


@router.post("/start")
async def start_training(request: TrainingRequest):
    """Start training with given data and hyperparameters"""

    trainer = get_trainer()
    if trainer.is_training:
        return {"error": "training already in progress"}

    try:
        # resolve data path - try relative to backend dir first
        data_path = Path(request.data_path)
        if not data_path.is_absolute():
            # try backend/data_path
            data_path = BACKEND_DIR / request.data_path
            if not data_path.exists():
                # try backend/training_data.jsonl
                data_path = BACKEND_DIR / "training_data.jsonl"

        logger.info(f"looking for training data at: {data_path}")

        if not data_path.exists():
            return {"error": f"training data not found at {data_path}"}

        # log data info
        with open(data_path, 'r') as f:
            num_lines = sum(1 for line in f if line.strip())
        logger.info(f"found {num_lines} training examples")

        # create config from request
        config = TrainingConfig(
            learning_rate=request.params.learning_rate,
            batch_size=request.params.batch_size,
            epochs=request.params.epochs,
            temperature=request.params.temperature,
            top_p=request.params.top_p,
        )

        # start training in background with error handling
        async def train_with_error_handling():
            try:
                await trainer.train(str(data_path), config)
            except Exception as e:
                logger.error(f"training failed: {e}")
                trainer.is_training = False

        asyncio.create_task(train_with_error_handling())

        return {
            "status": "training started",
            "config": config.__dict__,
            "data_path": str(data_path),
            "num_examples": num_lines
        }

    except Exception as e:
        logger.error(f"failed to start training: {e}")
        return {"error": str(e)}


@router.post("/pause")
async def pause_training():
    """Pause training"""
    trainer = get_trainer()
    trainer.pause()
    return {"status": "paused"}


@router.post("/resume")
async def resume_training():
    """Resume training"""
    trainer = get_trainer()
    trainer.resume()
    return {"status": "resumed"}


@router.post("/stop")
async def stop_training():
    """Stop training"""
    trainer = get_trainer()
    trainer.stop()
    return {"status": "stopped"}


@router.post("/checkpoint")
async def save_checkpoint():
    """Save model checkpoint"""
    try:
        import time
        trainer = get_trainer()
        timestamp = int(time.time())
        checkpoint_path = f"./checkpoints/checkpoint_{timestamp}"
        trainer.save_checkpoint(checkpoint_path)
        return {
            "status": "checkpoint saved",
            "path": checkpoint_path
        }
    except Exception as e:
        logger.error(f"failed to save checkpoint: {e}")
        return {"error": str(e)}


@router.get("/status")
async def get_status():
    """Get current training status"""
    trainer = get_trainer()
    return trainer.get_status()


@router.websocket("/stream")
async def stream_metrics(websocket: WebSocket):
    """WebSocket endpoint to stream real-time training metrics"""
    await websocket.accept()

    trainer = get_trainer()
    try:
        # create queue for metrics
        metrics_queue = asyncio.Queue()

        # set callback
        async def metrics_callback(metrics):
            await metrics_queue.put(metrics)

        # update trainer callback
        trainer.metrics_callback = metrics_callback

        # stream metrics while training
        while trainer.is_training or not metrics_queue.empty():
            try:
                # get metrics with timeout
                metrics = await asyncio.wait_for(
                    metrics_queue.get(),
                    timeout=1.0
                )

                # send to client
                await websocket.send_json({
                    "epoch": metrics.epoch,
                    "step": metrics.step,
                    "loss": metrics.loss,
                    "throughput": metrics.throughput,
                    "total_loss": metrics.total_loss,
                    "total_tokens": metrics.total_tokens,
                })

            except asyncio.TimeoutError:
                # send status even if no metrics
                status = trainer.get_status()
                await websocket.send_json({
                    "status": status
                })

            except Exception as e:
                logger.error(f"websocket error: {e}")
                break

    except WebSocketDisconnect:
        logger.info("client disconnected")

    except Exception as e:
        logger.error(f"websocket error: {e}")
        await websocket.close()
