"""
Pipeline.OS Backend - FastAPI Application
Local LLM Training Orchestrator & Dashboard API
"""

from fastapi import FastAPI, WebSocketException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes import training, checkpoints, ws
from app.config import settings
from app.db.database import engine, Base

# Initialize database tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifespan - startup and shutdown tasks"""
    # Startup
    print("🚀 Pipeline.OS Backend starting...")
    yield
    # Shutdown
    print("🛑 Pipeline.OS Backend shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Pipeline.OS",
    description="Local LLM Training Dashboard API",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(training.router, prefix="/api/training", tags=["training"])
app.include_router(checkpoints.router, prefix="/api/checkpoints", tags=["checkpoints"])
app.include_router(ws.router, prefix="/ws", tags=["websocket"])


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Pipeline.OS Backend",
        "version": "0.1.0"
    }


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Pipeline.OS Backend",
        "description": "Local LLM Training Orchestrator",
        "docs": "/docs",
        "version": "0.1.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )

