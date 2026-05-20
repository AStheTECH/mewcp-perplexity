import logging
from typing import Any, Dict, List, Optional

import httpx
from fastmcp_credentials import get_credentials

from .config import PERPLEXITY_CHAT_ENDPOINT, PERPLEXITY_MODELS_ENDPOINT
from .schemas import ModelInfo, PerplexityRequest, PerplexityResponse

logger = logging.getLogger("perplexity-mcp-server")


class PerplexityClient:
    """Client for Perplexity AI API."""

    def __init__(self):
        cred = get_credentials()
        api_key = cred.fields.get("api_key")
        if not api_key:
            raise ValueError("No 'api_key' found in credentials")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
    ) -> Dict[str, Any]:
        request_body: PerplexityRequest = {
            "model": model,
            "messages": messages,
        }

        if max_tokens is not None:
            request_body["max_tokens"] = max_tokens
        if temperature is not None:
            request_body["temperature"] = temperature
        if top_p is not None:
            request_body["top_p"] = top_p
        if top_k is not None:
            request_body["top_k"] = top_k
        if presence_penalty is not None:
            request_body["presence_penalty"] = presence_penalty
        if frequency_penalty is not None:
            request_body["frequency_penalty"] = frequency_penalty

        async with httpx.AsyncClient() as client:
            response = await client.post(
                PERPLEXITY_CHAT_ENDPOINT,
                headers=self.headers,
                json=request_body,
                timeout=60.0,
            )
            response.raise_for_status()
            return response.json()

    async def list_models(self) -> List[ModelInfo]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                PERPLEXITY_MODELS_ENDPOINT,
                headers=self.headers,
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])


async def search_perplexity(
    query: str,
    model: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
) -> Dict[str, Any]:
    from .config import DEFAULT_MODEL

    client = PerplexityClient()

    messages = [
        {
            "role": "user",
            "content": query,
        }
    ]

    return await client.chat_completion(
        messages=messages,
        model=model or DEFAULT_MODEL,
        max_tokens=max_tokens,
        temperature=temperature,
    )


async def get_available_models() -> List[ModelInfo]:
    client = PerplexityClient()
    return await client.list_models()
