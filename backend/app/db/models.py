"""
SQLAlchemy database models for persistence
"""

from sqlalchemy import Column, String, DateTime, Integer, Float, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


class TrainingRun(Base):
    """Database model for training runs"""
    __tablename__ = "training_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    model_name = Column(String, nullable=False)
    dataset_name = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, running, paused, completed, failed

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)

    # Training progress
    current_epoch = Column(Integer, default=0)
    total_epochs = Column(Integer, default=10)
    current_step = Column(Integer, default=0)
    total_steps = Column(Integer, default=10000)
    best_loss = Column(Float, default=float('inf'))

    # Hyperparameters (stored as JSON)
    hyperparameters = Column(JSON, nullable=False)

    # Relationships
    checkpoints = relationship("Checkpoint", back_populates="training", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "model_name": self.model_name,
            "dataset_name": self.dataset_name,
            "status": self.status,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "current_epoch": self.current_epoch,
            "total_epochs": self.total_epochs,
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "best_loss": self.best_loss,
            "hyperparameters": self.hyperparameters,
        }


class Checkpoint(Base):
    """Database model for training checkpoints"""
    __tablename__ = "checkpoints"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    training_id = Column(String, ForeignKey("training_runs.id"), nullable=False)

    # Training state at checkpoint
    step = Column(Integer, nullable=False)
    epoch = Column(Integer, nullable=False)
    loss = Column(Float, nullable=False)
    perplexity = Column(Float, nullable=False)

    # Checkpoint metadata
    saved_at = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String, nullable=False)  # Path to checkpoint file
    metadata = Column(JSON, nullable=True)  # Additional metadata

    # Relationship
    training = relationship("TrainingRun", back_populates="checkpoints")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "training_id": self.training_id,
            "step": self.step,
            "epoch": self.epoch,
            "loss": self.loss,
            "perplexity": self.perplexity,
            "saved_at": self.saved_at,
            "file_path": self.file_path,
            "metadata": self.metadata,
        }

