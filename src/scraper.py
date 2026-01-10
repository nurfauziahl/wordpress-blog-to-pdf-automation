from __future__ import annotations

import time
from typing import List, Set
from urllib.parse import urljoin, urlparse, parse_qs

import requests
from bs4 import BeautifulSoup


# -------------------------
# Helper functions
# -------------------------

def is_same_domain(url: str, root_domain: str) -> bool:
    return urlparse(url).netloc.endswith(root_domain)


def normalize_url(url: str) -> str:
    url = url.split("#")[0]
    if url.endswith("/"):
        url = url[:-1]
    return url


def is_post_url(url: str) -> bool:
    """
    Filter hanya URL artikel WordPress.
    Contoh valid: https://thomashealthblog.com/?p=21654
    """
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    # Artikel WordPress klasik punya parameter ?p=<id>
    return "p" in qs and qs["p"][0].isdigit()


# -------------------------
# Network
# -------------------------

def fetch_html(url: str, timeout: int = 30) -> str | None:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        print(f"[SKIP] Failed to fetch {url} ({e})")
        return None


# -------------------------
# Parsing
# -------------------------

def extract_links_from_page(html: str, base_url: str, root_domain: str) -> Set[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: Set[str] = set()

    for a in soup.select("a[href]"):
        href = a.get("href", "").strip()
        if not href:
            continue

        full_url = normalize_url(urljoin(base_url, href))

        if not is_same_domain(full_url, root_domain):
            continue

        if is_post_url(full_url):
            links.add(full_url)

    return links


# -------------------------
# Crawl
# -------------------------

def crawl(
    start_url: str,
    root_domain: str,
    max_pages: int = 20,
    delay_sec: float = 0.5,
) -> List[str]:
    visited: Set[str] = set()
    queue: List[str] = [normalize_url(start_url)]
    post_urls: Set[str] = set()

    while queue and len(post_urls) < max_pages:
        current_url = queue.pop(0)

        if current_url in visited:
            continue

        print(f"Fetching: {current_url}")
        visited.add(current_url)

        html = fetch_html(current_url)
        if not html:
            continue

        new_links = extract_links_from_page(
            html=html,
            base_url=current_url,
            root_domain=root_domain,
        )

        for link in new_links:
            if link not in post_urls:
                post_urls.add(link)

        time.sleep(delay_sec)

    return sorted(post_urls)
