"""Pulls the latest offsets JSON from the pinned gist and caches it."""
from __future__ import annotations

import json
from pathlib import Path

import requests
from loguru import logger

OFFSETS_SOURCE = "https://raw.githubusercontent.com/cs2-ext-esp-aim/offsets/main/latest.json"
CACHE = Path("offsets/latest.json")


def sync(timeout: float = 5.0) -> dict[str, int] | None:
    try:
        r = requests.get(OFFSETS_SOURCE, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(data, indent=2))
        logger.info("offsets synced build={}", data.get("build"))
        return data.get("offsets")
    except Exception as exc:  # noqa: BLE001
        logger.warning("offset sync failed: {}", exc)
        return None