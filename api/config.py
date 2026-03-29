import os

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
LLM_MODEL: str = os.getenv("LLM_MODEL", "claude-sonnet-4-6")
LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", "2"))
LLM_TIMEOUT: float = float(os.getenv("LLM_TIMEOUT", "30"))
REQUEST_TIMEOUT: float = float(os.getenv("REQUEST_TIMEOUT", "60"))

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIMENSIONS: int = int(os.getenv("EMBEDDING_DIMENSIONS", "1024"))

QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "rule_based_recursive")
RETRIEVER_TOP_K: int = int(os.getenv("RETRIEVER_TOP_K", "5"))
