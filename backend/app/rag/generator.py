from typing import Dict, Any, List, Optional
import json
import urllib.request
import urllib.error

from app.core.config import OLLAMA_BASE_URL, MODEL_NAME
from app.core.logging import logger
from app.rag.retriever import retrieve
from app.utils.helpers import truncate_text


def _call_ollama(prompt: str) -> str:
    """Call Ollama's /api/chat endpoint directly (no extra dependencies)."""
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = json.dumps({
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are InfoFlow AI, an enterprise internal knowledge assistant. "
                    "Answer questions accurately using only the provided context."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 1024,
        },
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["message"]["content"]


def build_prompt(query: str, context_chunks: List[Dict[str, Any]]) -> str:
    context_text = "\n\n".join(
        f"[{chunk['source']}] {chunk['text']}" for chunk in context_chunks
    )
    context_text = truncate_text(context_text)
    return (
        f"Context:\n{context_text}\n\n"
        f"Question:\n{query}\n\n"
        "Instructions:\n"
        "Answer using only the provided context. "
        "If the answer is not found in the context, say 'I do not know based on the available documents.'"
    )


def generate_answer(query: str) -> Dict[str, Any]:
    """Retrieve context and generate an answer using Ollama (local LLM)."""
    chunks = retrieve(query)
    if not chunks:
        return {
            "answer": "I do not know based on the available documents.",
            "sources": [],
        }

    prompt = build_prompt(query, chunks)
    sources = list({chunk["source"] for chunk in chunks})

    try:
        answer = _call_ollama(prompt)
    except Exception as e:
        logger.error(f"Ollama API error: {e}")
        answer = "An error occurred while generating the answer. Please try again later."

    return {"answer": answer, "sources": sources}
