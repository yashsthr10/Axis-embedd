"""End-to-end preprocessing pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dataset.clean.text_cleaner import clean_text, is_valid_text
from dataset.dedupe.exact_dedupe import dedupe_records
from dataset.preprocess.inspect import inspect_dataset, load_jsonl, save_jsonl
from dataset.preprocess.length_analysis import analyze_lengths, recommend_max_seq_length


@dataclass
class PreprocessConfig:
    input_path: Path = field(default_factory=lambda: Path("data/raw/documents.jsonl"))
    cleaned_path: Path = field(default_factory=lambda: Path("data/cleaned/documents.jsonl"))
    deduped_path: Path = field(default_factory=lambda: Path("data/deduped/documents.jsonl"))
    stats_path: Path = field(default_factory=lambda: Path("data/processed/stats.json"))
    min_chars: int = 50
    min_words: int = 10


@dataclass
class PreprocessResult:
    inspection: dict[str, Any]
    cleaning: dict[str, Any]
    deduplication: dict[str, Any]
    length_analysis: dict[str, float | int]
    recommended_max_seq_length: int
    cleaned_path: Path
    deduped_path: Path
    stats_path: Path


def run_preprocess(config: PreprocessConfig) -> PreprocessResult:
    raw_records = load_jsonl(config.input_path)
    inspection = inspect_dataset(raw_records)

    cleaned_records = []
    rejected_short = 0
    for record in raw_records:
        text = clean_text(record.get("text", ""))
        if not is_valid_text(text, min_chars=config.min_chars, min_words=config.min_words):
            rejected_short += 1
            continue
        cleaned_records.append({**record, "text": text, "char_count": len(text)})

    deduped_records, dedupe_stats = dedupe_records(cleaned_records)
    length_stats = analyze_lengths(records=deduped_records)
    recommended = recommend_max_seq_length(int(length_stats["p95_words"]))

    for path in (config.cleaned_path, config.deduped_path, config.stats_path):
        path.parent.mkdir(parents=True, exist_ok=True)

    save_jsonl(cleaned_records, config.cleaned_path)
    save_jsonl(deduped_records, config.deduped_path)

    result = PreprocessResult(
        inspection=inspection,
        cleaning={
            "input_count": len(raw_records),
            "output_count": len(cleaned_records),
            "rejected_short": rejected_short,
            "rejection_ratio": rejected_short / len(raw_records) if raw_records else 0.0,
        },
        deduplication=dedupe_stats,
        length_analysis=length_stats,
        recommended_max_seq_length=recommended,
        cleaned_path=config.cleaned_path,
        deduped_path=config.deduped_path,
        stats_path=config.stats_path,
    )

    stats = {
        "inspection": result.inspection,
        "cleaning": result.cleaning,
        "deduplication": result.deduplication,
        "length_analysis": result.length_analysis,
        "recommended_max_seq_length": result.recommended_max_seq_length,
        "paths": {
            "raw": str(config.input_path),
            "cleaned": str(config.cleaned_path),
            "deduped": str(config.deduped_path),
        },
    }
    config.stats_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    return result
