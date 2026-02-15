"""
Pipeline.OS Backend - FastAPI Application
Local LLM Training Orchestrator & Dashboard API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import training
from app.routes import chat
from app.routes import lora
from app.config import settings


# Create FastAPI app
app = FastAPI(
    title="pipelinex",
    description="local llm training dashboard api",
    version="0.1.0"
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
app.include_router(training.router, prefix="/api", tags=["training"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(lora.router, prefix="/api", tags=["lora"])


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
        ".docs": "/.docs",
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

