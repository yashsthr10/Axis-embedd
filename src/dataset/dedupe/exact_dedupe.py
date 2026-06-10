"""Exact deduplication for text records."""

from __future__ import annotations

import hashlib
from typing import Any


def normalize_for_dedupe(text: str) -> str:
    return text.strip().lower()


def text_hash(text: str) -> str:
    normalized = normalize_for_dedupe(text)
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()


def dedupe_records(
    records: list[dict[str, Any]],
    text_key: str = "text",
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Remove exact duplicate texts, keeping the first occurrence."""
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    duplicates = 0

    for record in records:
        text = record.get(text_key, "")
        digest = text_hash(text)
        if digest in seen:
            duplicates += 1
            continue
        seen.add(digest)
        unique.append(record)

    stats = {
        "input_count": len(records),
        "output_count": len(unique),
        "duplicates_removed": duplicates,
        "dedupe_ratio": duplicates / len(records) if records else 0.0,
    }
    return unique, stats
