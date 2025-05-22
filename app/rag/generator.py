import os
import requests
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_explanation(query: str, context: str, provider: str, model: str) -> str:
    prompt = (
        "You are an expert tutor. Use the following context to explain the topic "
        f'"{query}" to a beginner:\n\n'
        f"Context:\n{context}\n\n"
        "Explanation:\n"
    )
    if provider == "openai":
        return _generate_with_openai(prompt, model)
    elif provider == "ollama":
        return _generate_with_ollama(prompt, model)
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")


def _generate_with_openai(prompt: str, model: str) -> str:
    response = openai.responses.create(
        model=model,
        input=prompt,
    )
    return response.output_text


def _generate_with_ollama(prompt: str, model: str) -> str:
    url = f"http://host.docker.internal:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("response", "")