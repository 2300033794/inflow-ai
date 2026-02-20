import os
from pathlib import Path
from typing import List, Dict, Any

from app.utils.helpers import clean_text
from app.core.logging import logger


def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def load_pdf(file_path: str) -> str:
    try:
        import PyPDF2
        text_parts = []
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text_parts.append(page_text)
        return "\n".join(text_parts)
    except Exception as e:
        logger.error(f"Failed to load PDF {file_path}: {e}")
        return ""


def load_docx(file_path: str) -> str:
    try:
        from docx import Document
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    except Exception as e:
        logger.error(f"Failed to load DOCX {file_path}: {e}")
        return ""


def load_csv(file_path: str) -> str:
    try:
        import pandas as pd
        df = pd.read_csv(file_path)
        return df.to_string(index=False)
    except Exception as e:
        logger.error(f"Failed to load CSV {file_path}: {e}")
        return ""


LOADERS = {
    ".txt": load_txt,
    ".pdf": load_pdf,
    ".docx": load_docx,
    ".csv": load_csv,
}


def load_documents(data_path: str) -> List[Dict[str, Any]]:
    """Load all supported documents from the data directory."""
    documents = []
    data_dir = Path(data_path)
    if not data_dir.exists():
        logger.warning(f"Data directory not found: {data_path}")
        return documents

    for file_path in data_dir.iterdir():
        suffix = file_path.suffix.lower()
        if suffix not in LOADERS:
            continue
        logger.info(f"Loading {file_path.name}")
        raw_text = LOADERS[suffix](str(file_path))
        cleaned = clean_text(raw_text)
        if cleaned:
            documents.append({"source": file_path.name, "text": cleaned})
        else:
            logger.warning(f"No text extracted from {file_path.name}")

    logger.info(f"Loaded {len(documents)} documents from {data_path}")
    return documents
