from typing import Dict, Any, List, Optional

from openai import OpenAI

from app.core.config import OPENAI_API_KEY, MODEL_NAME
from app.core.logging import logger
from app.rag.retriever import retrieve
from app.utils.helpers import truncate_text

_client: Optional[OpenAI] = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


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
    """Retrieve context and generate an answer using OpenAI."""
    chunks = retrieve(query)
    if not chunks:
        return {
            "answer": "I do not know based on the available documents.",
            "sources": [],
        }

    prompt = build_prompt(query, chunks)
    sources = list({chunk["source"] for chunk in chunks})

    try:
        client = get_client()
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are InfoFlow AI, an enterprise internal knowledge assistant. "
                        "Answer questions accurately using only the provided context."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=1024,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        answer = "An error occurred while generating the answer. Please try again later."

    return {"answer": answer, "sources": sources}
