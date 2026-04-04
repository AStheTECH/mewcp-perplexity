# Perplexity MCP Server

A Model Context Protocol (MCP) server that provides access to Perplexity AI's API for web-search augmented LLM responses.

## Authentication

This server requires a Perplexity API key for authentication. You can obtain one from [Perplexity AI's dashboard](https://www.perplexity.ai/settings/api).

**Auth Model**: API key must be provided with every tool call (per-request authentication). The server is stateless and does not store authentication credentials between requests.

**MCP Type**: Utility (API key required per call, no multi-tenant session state)

## Available Tools

### Search & Query Tools

#### `search`
Perform a web search using Perplexity AI's online LLM models. Returns an AI-generated response with citations from online sources. Ideal for queries requiring current information, news, research, or factual answers with references.

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `api_key` | string | ✅ Yes | Perplexity API key for authentication |
| `query` | string | ✅ Yes | Search query to look up on the web |
| `model` | string | ❌ No | Model to use. Default: `llama-3.1-sonar-small-128k-online`. Options: `llama-3.1-sonar-small-128k-online`, `llama-3.1-sonar-large-128k-online`, `llama-3.1-sonar-huge-128k-online` |
| `max_tokens` | integer | ❌ No | Maximum tokens in response. Range: 1-4096 |
| `temperature` | float | ❌ No | Sampling temperature (0-2). Higher = more random, lower = more deterministic |

**Example**:
```json
{
  "tool": "search",
  "arguments": {
    "api_key": "pplx-your-api-key-here",
    "query": "What are the latest developments in quantum computing?",
    "model": "llama-3.1-sonar-large-128k-online",
    "max_tokens": 1000,
    "temperature": 0.7
  }
}