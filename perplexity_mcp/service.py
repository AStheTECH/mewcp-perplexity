import logging
from typing import Any, Dict, List, Optional

import httpx

from .config import PERPLEXITY_CHAT_ENDPOINT, PERPLEXITY_MODELS_ENDPOINT
from .schemas import ModelInfo, PerplexityRequest, PerplexityResponse

logger = logging.getLogger("perplexity-mcp-server")


class PerplexityClient:
    """Client for Perplexity AI API."""

    def __init__(self, api_key: str):
        """Initialize Perplexity API client.

        Args:
            api_key: Perplexity API key for authentication
        """
        self.api_key = api_key
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
        """Send chat completion request to Perplexity API.

        Args:
            messages: List of message objects with 'role' and 'content'
            model: Model ID to use
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-2)
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            presence_penalty: Presence penalty (-2 to 2)
            frequency_penalty: Frequency penalty (-2 to 2)

        Returns:
            API response as dictionary

        Raises:
            httpx.HTTPError: If API request fails
        """
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
                timeout=60.0,  # Perplexity can take time for online search
            )
            response.raise_for_status()
            return response.json()

    async def list_models(self) -> List[ModelInfo]:
        """List available models from Perplexity API.

        Returns:
            List of model information dictionaries

        Raises:
            httpx.HTTPError: If API request fails
        """
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
    api_key: str,
    query: str,
    model: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
) -> Dict[str, Any]:
    """Perform a search using Perplexity API.

    Args:
        api_key: Perplexity API key
        query: Search query string
        model: Model to use (defaults to online search model)
        max_tokens: Maximum tokens in response
        temperature: Sampling temperature

    Returns:
        API response dictionary
    """
    from .config import DEFAULT_MODEL

    client = PerplexityClient(api_key)

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


async def get_available_models(api_key: str) -> List[ModelInfo]:
    """Get list of available models from Perplexity.

    Args:
        api_key: Perplexity API key

    Returns:
        List of model information
    """
    client = PerplexityClient(api_key)
    return await client.list_models()
