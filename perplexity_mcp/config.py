import logging

# Perplexity API Configuration
PERPLEXITY_API_BASE = "https://api.perplexity.ai"
PERPLEXITY_CHAT_ENDPOINT = f"{PERPLEXITY_API_BASE}/chat/completions"
PERPLEXITY_MODELS_ENDPOINT = f"{PERPLEXITY_API_BASE}/models"

# Default model for online search
DEFAULT_MODEL = "llama-3.1-sonar-small-128k-online"

# Available online models (for reference)
AVAILABLE_ONLINE_MODELS = [
    "llama-3.1-sonar-small-128k-online",
    "llama-3.1-sonar-large-128k-online",
    "llama-3.1-sonar-huge-128k-online",
]


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
