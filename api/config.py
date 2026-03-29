import os

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
LLM_MODEL: str = os.getenv("LLM_MODEL", "claude-sonnet-4-6")
LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", "2"))
LLM_TIMEOUT: float = float(os.getenv("LLM_TIMEOUT", "30"))
REQUEST_TIMEOUT: float = float(os.getenv("REQUEST_TIMEOUT", "60"))
