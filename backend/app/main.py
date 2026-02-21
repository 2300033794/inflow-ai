import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import logger
from app.core.config import CORS_ORIGINS, VECTOR_DB_PATH, DATA_PATH, validate_config
from app.api.routes import chat, ingest, health

# Validate configuration and ensure required directories exist
validate_config()
os.makedirs(VECTOR_DB_PATH, exist_ok=True)
os.makedirs(DATA_PATH, exist_ok=True)

app = FastAPI(
    title="InfoFlow AI",
    description="Enterprise Internal Knowledge Assistant powered by RAG",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(ingest.router, tags=["Ingest"])

logger.info("InfoFlow AI application started.")
