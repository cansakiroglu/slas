from fastapi import APIRouter
import requests
import openai

router = APIRouter()


@router.get("/openai-models")
async def get_openai_models():
    """Endpoint to fetch available OpenAI models."""

    return {
        "models": [
            model.id
            for model in openai.models.list().data
            if model.id.startswith("gpt")
            and not any(
                excluded in model.id
                for excluded in ["preview", "transcribe", "audio", "image", "tts"]
            )
        ]
    }


@router.get("/ollama-models")
async def get_ollama_models():
    """Endpoint to fetch available Ollama models."""

    response = requests.get("http://host.docker.internal:11434/api/tags")
    if response.status_code == 200:
        data = response.json()["models"]
        return {"models": [model["name"] for model in data]}
    else:
        raise Exception(
            "Failed to fetch Ollama models. Please ensure the Ollama server is running."
        )
