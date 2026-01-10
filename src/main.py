from __future__ import annotations

from pathlib import Path

from .wp_api import fetch_post_links
from .renderer import url_to_pdf
from .merger import merge_pdfs
from .utils import slugify_url


def main() -> None:
    pdf_dir = Path("data/intermediate/pdf")
    merged_pdf = Path("data/output/drthomashealthblog-full.pdf")

    # 1) Ambil URL post dari WordPress REST API
    # max_pages=1 untuk testing (page 1 saja). Nanti hapus/ubah jadi None untuk ambil semua.
    urls = fetch_post_links(per_page=100, delay_sec=0.2, max_pages=1)
    print(f"Collected {len(urls)} post URLs from WP API")

    # TEST MODE: batasi render agar cepat dan aman
    urls = urls[:10]
    print("Testing with first 10 URLs only.")

    # 2) Render tiap URL menjadi PDF
    pdf_paths: list[Path] = []

    for i, url in enumerate(urls, start=1):
        filename = f"{i:04d}-{slugify_url(url)}.pdf"
        out_pdf = pdf_dir / filename

        # Resume: jika file sudah ada, tidak render ulang
        if out_pdf.exists():
            print(f"[SKIP] Exists: {out_pdf}")
            pdf_paths.append(out_pdf)
            continue

        print(f"[{i}/{len(urls)}] Rendering: {url} -> {out_pdf}")

        try:
            url_to_pdf(url, out_pdf, wkhtmltopdf_path=None)  # isi path jika pdfkit tidak menemukan wkhtmltopdf
            pdf_paths.append(out_pdf)
        except Exception as e:
            print(f"[SKIP] Render failed for {url}: {e}")

    # 3) Merge hanya jika ada PDF yang berhasil
    if not pdf_paths:
        print("No PDFs generated. Skipping merge.")
        return

    print(f"Merging {len(pdf_paths)} PDFs -> {merged_pdf}")
    merge_pdfs(pdf_paths, merged_pdf)
    print("DONE")


if __name__ == "__main__":
    main()
