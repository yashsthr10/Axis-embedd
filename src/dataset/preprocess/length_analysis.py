"""Token/ word length analysis for max_seq_length decisions."""

from __future__ import annotations

import math
from typing import Any


def word_count(text: str) -> int:
    return len(text.split())


def analyze_lengths(
    texts: list[str] | None = None,
    text_key: str | None = None,
    records: list[dict[str, Any]] | None = None,
) -> dict[str, float | int]:
    if records is not None:
        texts = [r[text_key or "text"] for r in records]
    if texts is None:
        texts = []

    if not texts:
        return {
            "count": 0,
            "min_words": 0,
            "mean_words": 0.0,
            "p50_words": 0,
            "p95_words": 0,
            "p99_words": 0,
            "max_words": 0,
        }

    lengths = sorted(word_count(t) for t in texts)
    n = len(lengths)

    def percentile(p: float) -> int:
        idx = min(int(math.ceil(p * n)) - 1, n - 1)
        return lengths[max(idx, 0)]

    return {
        "count": n,
        "min_words": lengths[0],
        "mean_words": round(sum(lengths) / n, 1),
        "p50_words": percentile(0.50),
        "p95_words": percentile(0.95),
        "p99_words": percentile(0.99),
        "max_words": lengths[-1],
    }


def recommend_max_seq_length(p95_words: int) -> int:
    """Round p95 word count up to a practical max_seq_length."""
    candidates = [64, 128, 256, 384, 512, 768, 1024, 1536, 2048, 3072, 4096]
    for candidate in candidates:
        if candidate >= p95_words:
            return candidate
    return int(math.ceil(p95_words / 512) * 512)
