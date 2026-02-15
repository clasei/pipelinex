"""
Pydantic models for API request/response validation
These define the contract between frontend and backend
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TrainingStatus(str, Enum):
    """Training run status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class HyperParametersModel(BaseModel):
    """Hyperparameters configuration"""
    temperature: float = Field(default=0.7, ge=0, le=2.0)
    top_p: float = Field(default=0.95, ge=0, le=1.0)
    learning_rate: str = Field(default="5e-5")
    batch_size: int = Field(default=128, ge=1)
    epochs: int = Field(default=10, ge=1)
    use_lora: bool = Field(default=True)
    quantization: bool = Field(default=False)

    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 0.7,
                "top_p": 0.95,
                "learning_rate": "5e-5",
                "batch_size": 128,
                "epochs": 10,
                "use_lora": True,
                "quantization": False
            }
        }


class CheckpointResponse(BaseModel):
    """Checkpoint metadata response"""
    id: str
    training_id: str
    step: int
    epoch: int
    loss: float
    perplexity: float
    saved_at: datetime
    file_path: str
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class TrainingStatsModel(BaseModel):
    """Real-time training statistics"""
    epoch: int
    total_epochs: int
    step: int
    total_steps: int
    loss: float
    perplexity: float
    throughput: int  # tokens per second

    class Config:
        json_schema_extra = {
            "example": {
                "epoch": 3,
                "total_epochs": 10,
                "step": 4250,
                "total_steps": 10000,
                "loss": 0.0412,
                "perplexity": 1.04,
                "throughput": 1450
            }
        }


class CreateTrainingRequest(BaseModel):
    """Request to start a new training run"""
    model_name: str = Field(..., min_length=1)
    dataset_name: str = Field(..., min_length=1)
    hyperparameters: HyperParametersModel
    total_steps: int = Field(default=10000, ge=1)

    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "Llama-3-Surf-Instruct",
                "dataset_name": "hack_v2",
                "hyperparameters": {
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "learning_rate": "5e-5",
                    "batch_size": 128,
                    "epochs": 10,
                    "use_lora": True,
                    "quantization": False
                },
                "total_steps": 10000
            }
        }


class TrainingResponse(BaseModel):
    """Training run response"""
    id: str
    model_name: str
    dataset_name: str
    status: TrainingStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    current_epoch: int = 0
    total_epochs: int = 10
    current_step: int = 0
    total_steps: int = 10000
    best_loss: float = float('inf')
    hyperparameters: HyperParametersModel
    checkpoints: Optional[list[CheckpointResponse]] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "train_abc123",
                "model_name": "Llama-3-Surf-Instruct",
                "dataset_name": "hack_v2",
                "status": "running",
                "created_at": "2026-02-15T10:00:00Z",
                "started_at": "2026-02-15T10:05:00Z",
                "ended_at": None,
                "current_epoch": 3,
                "total_epochs": 10,
                "current_step": 4250,
                "total_steps": 10000,
                "best_loss": 0.0412,
                "hyperparameters": {
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "learning_rate": "5e-5",
                    "batch_size": 128,
                    "epochs": 10,
                    "use_lora": True,
                    "quantization": False
                },
                "checkpoints": []
            }
        }


class UpdateTrainingRequest(BaseModel):
    """Request to update training run (pause/resume/update params)"""
    status: Optional[TrainingStatus] = None
    hyperparameters: Optional[HyperParametersModel] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "paused",
                "hyperparameters": None
            }
        }


class SaveCheckpointRequest(BaseModel):
    """Request to save a checkpoint"""
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "metadata": {
                    "reason": "manual",
                    "notes": "End of epoch 3"
                }
            }
        }


class LogMessageModel(BaseModel):
    """Log message for streaming"""
    timestamp: datetime
    level: str  # INFO, WARN, ERROR, PROGRESS
    message: str
    metadata: Optional[str] = None


class WebSocketMessageModel(BaseModel):
    """Message format for WebSocket communication"""
    type: str  # "log", "stats", "error", "control"
    timestamp: datetime
    data: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "type": "stats",
                "timestamp": "2026-02-15T10:30:45Z",
                "data": {
                    "epoch": 3,
                    "step": 4250,
                    "loss": 0.0412,
                    "throughput": 1450
                }
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str

