import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "vector_store")
DATA_PATH: str = os.getenv("DATA_PATH", "data")
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))
TOP_K: int = int(os.getenv("TOP_K", "5"))
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")


def validate_config() -> None:
    """Fail fast if required configuration is missing."""
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
        raise RuntimeError(
            "OPENAI_API_KEY is not set. "
            "Please set it in your .env file or environment before starting the server."
        )
