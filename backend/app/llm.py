from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

# OpenAI config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

try:
    from openai import AsyncOpenAI
except Exception:  # pragma: no cover
    AsyncOpenAI = None  # type: ignore

# Azure AI Inference (GitHub Models) config
AZURE_INFERENCE_ENDPOINT = os.getenv("AZURE_INFERENCE_ENDPOINT", "https://models.github.ai/inference")
AZURE_INFERENCE_MODEL = os.getenv("AZURE_INFERENCE_MODEL", "mistral-ai/mistral-small-2503")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

try:
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
except Exception:  # pragma: no cover
    ChatCompletionsClient = None  # type: ignore
    SystemMessage = UserMessage = AzureKeyCredential = None  # type: ignore


async def async_generate_reasoning(prompt: str, system_message: str, model: Optional[str] = None) -> str:
    """Generate reasoning text using OpenAI (preferred) or Azure AI Inference based on available creds."""
    # Prefer OpenAI if available
    if OPENAI_API_KEY and AsyncOpenAI is not None:
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        used_model = model or OPENAI_MODEL
        resp = await client.chat.completions.create(
            model=used_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=300,
        )
        return (resp.choices[0].message.content or "").strip()

    # Fallback to Azure AI Inference (GitHub Models)
    if GITHUB_TOKEN and ChatCompletionsClient and AzureKeyCredential and SystemMessage and UserMessage:
        client = ChatCompletionsClient(
            endpoint=AZURE_INFERENCE_ENDPOINT,
            credential=AzureKeyCredential(GITHUB_TOKEN),
        )
        used_model = model or AZURE_INFERENCE_MODEL

        import asyncio

        def _call_sync() -> str:
            resp = client.complete(
                messages=[
                    SystemMessage(system_message),
                    UserMessage(prompt),
                ],
                temperature=0.2,
                top_p=1.0,
                max_tokens=300,
                model=used_model,
            )
            return (resp.choices[0].message.content or "").strip()

        return await asyncio.to_thread(_call_sync)

    # Final fallback
    return "Based on your query and the retrieved products, these seem like strong matches."


