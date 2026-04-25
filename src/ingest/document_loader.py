from pathlib import Path
from typing import Dict

import fitz  # PyMuPDF
from docx import Document


class DocumentLoader:
    """
    Load contract documents from PDF, DOCX, or TXT files and extract plain text.

    This module is the first step of the Research Contract Adviser Agent pipeline:
    document upload -> text extraction -> clause segmentation.
    """

    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

    def load(self, file_path: str) -> Dict[str, str]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {path.suffix}. "
                f"Supported types: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )

        if path.suffix.lower() == ".pdf":
            text = self._load_pdf(path)
        elif path.suffix.lower() == ".docx":
            text = self._load_docx(path)
        else:
            text = self._load_txt(path)

        return {
            "file_name": path.name,
            "file_type": path.suffix.lower(),
            "text": text.strip(),
        }

    def _load_pdf(self, path: Path) -> str:
        text_parts = []

        with fitz.open(path) as doc:
            for page_number, page in enumerate(doc, start=1):
                page_text = page.get_text("text")
                if page_text:
                    text_parts.append(f"\n[Page {page_number}]\n{page_text}")

        return "\n".join(text_parts)

    def _load_docx(self, path: Path) -> str:
        doc = Document(path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)

    def _load_txt(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")
