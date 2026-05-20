**Answer any question with live web search, citations, and AI reasoning — all in one call.**

A Model Context Protocol (MCP) server that exposes Perplexity AI's API for real-time web search and conversational queries with cited sources.


## Overview

The Perplexity MCP Server provides AI-powered web search with grounded, citation-backed responses:

- Query the live web and get LLM-synthesized answers with source references
- Control response length, temperature, and the underlying search model
- Browse available Perplexity models to choose the right capability for each task

Perfect for:

- Giving AI assistants access to current events, news, and real-time information
- Answering research questions that require up-to-date facts beyond the model's training cutoff
- Enriching AI workflows with cited, verifiable web sources


## Tools

<details>
<summary><code>health_check</code> — Check server readiness</summary>

Returns a status object confirming the server is running and reachable.

**Inputs:** _(none)_

**Output:**

```json
{
  "status": "ok",
  "server": "CL Perplexity MCP Server"
}
```

</details>


<details>
<summary><code>search</code> — Search the web with Perplexity AI</summary>

Sends a query to Perplexity's online search models and returns an LLM-generated answer with citations from live web sources.

**Inputs:**
```
- `query`       (string, required)  — Search query to look up on the web
- `model`       (string, optional)  — Model to use (default: llama-3.1-sonar-small-128k-online)
- `max_tokens`  (integer, optional) — Maximum tokens in the response, 1–4096
- `temperature` (float, optional)   — Sampling temperature 0–2; higher = more creative (default: model default)
```

**Output:**

```json
{
  "success": true,
  "query": "latest AI research papers 2025",
  "response": "Recent AI research has focused on...",
  "model": "llama-3.1-sonar-small-128k-online",
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 320,
    "total_tokens": 332
  }
}
```

</details>


<details>
<summary><code>get_models</code> — List available Perplexity models</summary>

Returns all models available through the Perplexity API, grouped into online (web search) and offline (non-search) categories.

**Inputs:** _(none)_

**Output:**

```json
{
  "success": true,
  "total_models": 6,
  "online_models": [
    "llama-3.1-sonar-small-128k-online",
    "llama-3.1-sonar-large-128k-online",
    "llama-3.1-sonar-huge-128k-online"
  ],
  "other_models": [
    "llama-3.1-sonar-small-128k-chat",
    "llama-3.1-sonar-large-128k-chat"
  ],
  "all_models": [...]
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Model Selection</strong></summary>

**Online models** (include live web search):

- `llama-3.1-sonar-small-128k-online` — Fast, cost-efficient; default for web search
- `llama-3.1-sonar-large-128k-online` — Higher quality answers, more thorough search
- `llama-3.1-sonar-huge-128k-online` — Best quality, most comprehensive; highest cost

Use `get_models` to retrieve the current full list — new models are added periodically.

</details>

<details>
<summary><strong>Generation Parameters</strong></summary>

- `temperature` — Controls randomness; `0.0` for focused factual answers, `1.0+` for creative responses (range: 0–2)
- `max_tokens` — Caps response length; useful for controlling cost and latency (range: 1–4096)

</details>


## Getting Your Perplexity API Key

<details>
<summary><strong>Steps</strong></summary>

1. Go to the [Perplexity API Settings](https://www.perplexity.ai/settings/api)
2. Sign in or create a Perplexity account
3. Under **API Keys**, click **+ Generate**
4. Copy the generated key — store it securely, it will not be shown again

> Perplexity API usage is billed per request based on the model and token count. Online models consume additional credits for web search.

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API key is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Perplexity credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Add your Perplexity API key
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure the `query` parameter is included and is a non-empty string
  3. Check that `temperature` is between 0.0 and 2.0 and `max_tokens` is between 1 and 4096

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Perplexity API Error</strong></summary>

- **Cause:** Upstream Perplexity API returned an error
- **Solution:**
  1. Check Perplexity service status at [Perplexity Status Page](https://status.perplexity.ai/)
  2. Verify your API key has sufficient credits for the selected model
  3. Review the error message for specific details (e.g. rate limit exceeded, invalid model ID)

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Perplexity API Documentation](https://docs.perplexity.ai/)** — Official API reference
- **[Perplexity Model Cards](https://docs.perplexity.ai/guides/model-cards)** — Model capabilities and pricing
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
