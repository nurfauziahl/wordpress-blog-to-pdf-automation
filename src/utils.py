from __future__ import annotations

import re
from urllib.parse import urlparse, parse_qs


def slugify_url(url: str) -> str:
    """
    Buat nama file yang unik dari URL.

    Prioritas:
    1) Jika URL WordPress punya ?p=<id>, gunakan p-<id> (paling stabil & unik).
    2) Jika tidak, gunakan path (mis. /some-post-title).
    3) Jika kosong, fallback "home".
    """
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    # WordPress post ID (stabil, unik)
    if "p" in qs and qs["p"] and qs["p"][0].isdigit():
        return f"p-{qs['p'][0]}"

    # gunakan path
    path = parsed.path.strip("/")
    if not path:
        return "home"

    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", path).strip("-").lower()
    return slug[:150]
