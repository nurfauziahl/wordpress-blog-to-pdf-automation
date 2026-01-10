from __future__ import annotations

from pathlib import Path
from typing import List

from pypdf import PdfWriter


def merge_pdfs(pdf_paths: List[Path], output_pdf: Path) -> None:
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    writer = PdfWriter()
    for p in pdf_paths:
        writer.append(str(p))

    with open(output_pdf, "wb") as f:
        writer.write(f)
