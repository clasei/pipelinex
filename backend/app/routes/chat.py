"""
Chat endpoint to interact with trained Ollama model
"""
from fastapi import APIRouter
from pydantic import BaseModel
import requests
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    model: str = "mistral:latest"


class ChatResponse(BaseModel):
    response: str
    model: str


@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a message to the trained Ollama model"""

    try:
        ollama_url = "http://localhost:11434"

        # Send request to Ollama
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": request.model,
                "prompt": request.message,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.95,
                }
            },
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            model_response = data.get("response", "")

            logger.info(f"chat request processed: {len(model_response)} chars")

            return ChatResponse(
                response=model_response,
                model=request.model
            )
        else:
            logger.error(f"ollama error: {response.status_code}")
            return ChatResponse(
                response="Sorry, I encountered an error. Please make sure Ollama is running.",
                model=request.model
            )

    except requests.exceptions.Timeout:
        logger.warning("ollama request timeout")
        return ChatResponse(
            response="Request timed out. The model might be processing a large response.",
            model=request.model
        )
    except Exception as e:
        logger.error(f"chat error: {e}")
        return ChatResponse(
            response=f"Error: {str(e)}",
            model=request.model
        )

