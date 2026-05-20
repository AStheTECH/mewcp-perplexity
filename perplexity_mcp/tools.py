import json
import logging

from fastmcp import FastMCP
from pydantic import Field

from .service import get_available_models, search_perplexity

logger = logging.getLogger("perplexity-mcp-server")


def register_tools(mcp: FastMCP) -> None:
    """Register all Perplexity MCP tools."""

    @mcp.tool(
        name="search",
        description="Search the web using Perplexity AI. Returns an LLM-generated response with citations from online sources. Use this for queries that need current information, news, or factual answers with references.",
    )
    async def search(
        query: str = Field(..., description="Search query to look up on the web"),
        model: str = Field(
            default=None,
            description="Model to use (default: llama-3.1-sonar-small-128k-online). Available online models: llama-3.1-sonar-small-128k-online, llama-3.1-sonar-large-128k-online, llama-3.1-sonar-huge-128k-online",
        ),
        max_tokens: int = Field(
            default=None,
            description="Maximum number of tokens in the response",
            ge=1,
            le=4096,
        ),
        temperature: float = Field(
            default=None,
            description="Sampling temperature (0-2). Higher values make output more random, lower values more deterministic",
            ge=0.0,
            le=2.0,
        ),
    ) -> str:
        """Execute a web search using Perplexity AI."""
        try:
            logger.info(f"Executing search for query: {query[:100]}...")

            result = await search_perplexity(
                query=query,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            if "choices" in result and len(result["choices"]) > 0:
                response_text = result["choices"][0]["message"]["content"]

                output = {
                    "success": True,
                    "query": query,
                    "response": response_text,
                    "model": result.get("model"),
                    "usage": result.get("usage"),
                }

                logger.info(f"Search completed successfully for query: {query[:100]}...")
                return json.dumps(output, indent=2)
            else:
                error_msg = "Unexpected API response format"
                logger.error(f"Search failed for query '{query}': {error_msg}")
                return json.dumps({"success": False, "error": error_msg})

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Search failed for query '{query}': {error_msg}", exc_info=True)
            return json.dumps({"success": False, "error": error_msg, "query": query})

    @mcp.tool(
        name="get_models",
        description="List all available models from Perplexity AI, including both online and offline models.",
    )
    async def get_models() -> str:
        """Get list of available Perplexity models."""
        try:
            logger.info("Fetching available models...")

            models = await get_available_models()

            online_models = []
            other_models = []

            for model in models:
                model_id = model.get("id", "unknown")
                if "online" in model_id:
                    online_models.append(model_id)
                else:
                    other_models.append(model_id)

            output = {
                "success": True,
                "total_models": len(models),
                "online_models": online_models,
                "other_models": other_models,
                "all_models": [m.get("id") for m in models],
            }

            logger.info(f"Retrieved {len(models)} models")
            return json.dumps(output, indent=2)

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to fetch models: {error_msg}", exc_info=True)
            return json.dumps({"success": False, "error": error_msg})

    @mcp.tool(
        name="health_check",
        description="Check server readiness and basic connectivity.",
    )
    def health_check() -> str:
        return json.dumps({"status": "ok", "server": "CL Perplexity MCP Server"})
