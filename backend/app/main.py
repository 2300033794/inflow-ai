from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import logger
from app.core.config import CORS_ORIGINS
from app.api.routes import chat, ingest, health

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
