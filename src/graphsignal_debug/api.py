"""Client for Graphsignal API (api.graphsignal.com)."""

from datetime import datetime, timezone
from typing import Optional

import requests

from .config import DEFAULT_API_BASE


def iso_to_ns(iso_str: str) -> int:
    """Convert ISO 8601 datetime string (e.g. 2026-03-10T00:00:00Z) to nanoseconds since epoch."""
    s = iso_str.strip().replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1_000_000_000)


def fetch_debug_context(
    api_key: str,
    start_time_ns: int,
    end_time_ns: int,
    tags: Optional[str] = None,
    api_base: str = DEFAULT_API_BASE,
) -> str:
    """
    GET /api/v1/debug_context/ and return the 'context' field from the response.
    Raises requests.HTTPError on non-2xx.
    """
    url = f"{api_base.rstrip('/')}/api/v1/debug_context/"
    headers = {"X-API-KEY": api_key}
    params = {
        "start_time_ns": start_time_ns,
        "end_time_ns": end_time_ns,
    }
    if tags:
        params["tags"] = tags
    resp = requests.get(url, headers=headers, params=params, timeout=(5, 30))
    resp.raise_for_status()
    data = resp.json()
    return data.get("context", "")
