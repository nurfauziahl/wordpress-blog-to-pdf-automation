from __future__ import annotations

from typing import List, Optional
import time

import requests


BASE_REST_ROUTE = "https://thomashealthblog.com/index.php?rest_route="


def _default_headers() -> dict:
    # Header yang dibuat mirip browser agar tidak kena 406
    return {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://thomashealthblog.com/",
    }


def _make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(_default_headers())
    return s


def _get_total_pages(session: requests.Session, per_page: int = 100, timeout: int = 30) -> int:
    url = f"{BASE_REST_ROUTE}/wp/v2/posts&per_page={per_page}&page=1"
    r = session.get(url, timeout=timeout, allow_redirects=True)

    # Debug message yang jelas bila diblokir
    if r.status_code == 406:
        raise RuntimeError(
            "Got 406 Not Acceptable from server. "
            "This usually means the site blocks non-browser requests. "
            "Headers were set, but the site may require additional anti-bot measures."
        )

    r.raise_for_status()

    total_pages = r.headers.get("X-WP-TotalPages") or r.headers.get("x-wp-totalpages")
    if not total_pages:
        raise RuntimeError("Header X-WP-TotalPages not found. REST API may be restricted.")
    return int(total_pages)


def fetch_post_links(
    per_page: int = 100,
    timeout: int = 30,
    delay_sec: float = 0.2,
    max_pages: Optional[int] = None,
) -> List[str]:
    """
    Ambil semua link post dari WordPress REST API.
    Mengembalikan list URL artikel (field 'link').

    max_pages: batasi jumlah page API untuk testing (misal 1 atau 2). None = ambil semua.
    """
    session = _make_session()

    total_pages = _get_total_pages(session=session, per_page=per_page, timeout=timeout)
    if max_pages is not None:
        total_pages = min(total_pages, max_pages)

    links: List[str] = []

    for page in range(1, total_pages + 1):
        url = f"{BASE_REST_ROUTE}/wp/v2/posts&per_page={per_page}&page={page}"
        r = session.get(url, timeout=timeout, allow_redirects=True)

        if r.status_code == 406:
            print(f"[STOP] 406 Not Acceptable on page={page}. Try increasing headers/delay.")
            break

        r.raise_for_status()

        posts = r.json()
        for p in posts:
            link = p.get("link")
            if link:
                links.append(link)

        if delay_sec:
            time.sleep(delay_sec)

    # Dedup tanpa mengubah urutan
    seen = set()
    uniq: List[str] = []
    for u in links:
        if u not in seen:
            seen.add(u)
            uniq.append(u)

    return uniq
