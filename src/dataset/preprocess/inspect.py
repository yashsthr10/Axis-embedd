"""Dataset inspection utilities."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_jsonl(path: Path | str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def save_jsonl(records: list[dict[str, Any]], path: Path | str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def detect_format(records: list[dict[str, Any]]) -> str:
    """Classify dataset format to determine training strategy."""
    if not records:
        return "empty"

    sample = records[0]
    keys = set(sample.keys())

    if {"anchor", "positive"} <= keys or {"anchor", "positive", "negative"} <= keys:
        return "contrastive_triplet"
    if {"query", "document"} <= keys or {"query", "positive"} <= keys:
        return "query_document"
    if "text" in keys:
        return "single_text"
    return "unknown"


def inspect_dataset(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize schema, format, and basic stats."""
    if not records:
        return {"count": 0, "format": "empty", "fields": []}

    field_counts: Counter[str] = Counter()
    for record in records:
        field_counts.update(record.keys())

    sample = records[0]
    fmt = detect_format(records)

    training_note = {
        "single_text": (
            "Raw documents only. Contrastive query-document pairs must be "
            "generated in pair_generation/ before training."
        ),
        "query_document": "Ready for contrastive training (query -> positive document).",
        "contrastive_triplet": "Ready for triplet or InfoNCE contrastive training.",
        "unknown": "Schema unrecognized. Inspect fields manually.",
        "empty": "No records to inspect.",
    }[fmt]

    return {
        "count": len(records),
        "format": fmt,
        "fields": sorted(field_counts.keys()),
        "field_coverage": {k: field_counts[k] / len(records) for k in field_counts},
        "sample_keys": list(sample.keys()),
        "sample_preview": {k: str(sample[k])[:120] for k in sample},
        "training_strategy": training_note,
    }
