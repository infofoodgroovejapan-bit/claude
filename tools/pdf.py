"""PDF utility functions for attaching PDF files to Claude API requests."""
import base64
from pathlib import Path


def read_pdf_as_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def build_pdf_content_block(file_path: str) -> dict:
    return {
        "type": "document",
        "source": {
            "type": "base64",
            "media_type": "application/pdf",
            "data": read_pdf_as_base64(file_path),
        },
        "title": Path(file_path).name,
    }
