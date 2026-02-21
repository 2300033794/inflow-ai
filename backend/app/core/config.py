import os
from pathlib import Path
from dotenv import load_dotenv

# Resolve paths relative to the backend/ directory
_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(_BACKEND_DIR / ".env")

OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME: str = os.getenv("MODEL_NAME", "llama3.2")
VECTOR_DB_PATH: str = str(_BACKEND_DIR / os.getenv("VECTOR_DB_PATH", "data/vector_store"))
DATA_PATH: str = str(_BACKEND_DIR / os.getenv("DATA_PATH", "data"))
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))
TOP_K: int = int(os.getenv("TOP_K", "5"))
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")


def validate_config() -> None:
    """Check that Ollama is reachable."""
    import urllib.request
    try:
        urllib.request.urlopen(OLLAMA_BASE_URL, timeout=5)
    except Exception:
        raise RuntimeError(
            f"Cannot reach Ollama at {OLLAMA_BASE_URL}. "
            "Make sure Ollama is installed and running (run 'ollama serve' or start the Ollama app)."
        )
