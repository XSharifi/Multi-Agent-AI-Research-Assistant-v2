from pathlib import Path
import fitz
from langchain_core.tools import tool

@tool
def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from a PDF."""
    p = Path(pdf_path)
    if not p.exists():
        raise FileNotFoundError(pdf_path)
    d = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in d)
    d.close()
    return text
