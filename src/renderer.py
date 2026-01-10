from __future__ import annotations

from pathlib import Path
from typing import Optional

import pdfkit


def get_pdfkit_config(wkhtmltopdf_path: Optional[str] = None) -> Optional[pdfkit.configuration]:
    if wkhtmltopdf_path:
        return pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    return None


def url_to_pdf(url: str, out_pdf: Path, wkhtmltopdf_path: Optional[str] = None) -> None:
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    options = {
        "encoding": "UTF-8",
        "quiet": "",
    }

    config = get_pdfkit_config(wkhtmltopdf_path)
    pdfkit.from_url(url, str(out_pdf), options=options, configuration=config)
