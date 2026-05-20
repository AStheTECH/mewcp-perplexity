from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class PerplexityMessage(TypedDict, total=False):
    """Message structure for Perplexity API."""

    role: str  # 'system', 'user', 'assistant'
    content: str


class PerplexityRequest(TypedDict, total=False):
    """Request structure for Perplexity chat completion API."""

    model: str
    messages: List[PerplexityMessage]
    max_tokens: Optional[int]
    temperature: Optional[float]
    top_p: Optional[float]
    top_k: Optional[int]
    presence_penalty: Optional[float]
    frequency_penalty: Optional[float]


class PerplexityChoice(TypedDict):
    """Choice structure from Perplexity API response."""

    index: int
    message: PerplexityMessage
    finish_reason: str


class PerplexityUsage(TypedDict):
    """Token usage from Perplexity API response."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class PerplexityResponse(TypedDict, total=False):
    """Response structure from Perplexity API."""

    id: str
    model: str
    choices: List[PerplexityChoice]
    usage: PerplexityUsage
    created: int


class ModelInfo(TypedDict):
    """Model information from Perplexity API."""

    id: str
    object: str
    created: int
    owned_by: str


