#!/usr/bin/env python3
"""Run dataset inspection, cleaning, deduplication, and length analysis."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from dataset.paths import data_dir, resolve_repo_root
from dataset.preprocess.pipeline import PreprocessConfig, run_preprocess


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preprocess raw crawl data")
    parser.add_argument("--min-chars", type=int, default=50)
    parser.add_argument("--min-words", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = resolve_repo_root(REPO_ROOT)
    data = data_dir(root)

    config = PreprocessConfig(
        input_path=data / "raw" / "documents.jsonl",
        cleaned_path=data / "cleaned" / "documents.jsonl",
        deduped_path=data / "deduped" / "documents.jsonl",
        stats_path=data / "processed" / "stats.json",
        min_chars=args.min_chars,
        min_words=args.min_words,
    )

    if not config.input_path.exists():
        print(f"error: input not found: {config.input_path}", file=sys.stderr)
        return 1

    result = run_preprocess(config)
    stats = json.loads(config.stats_path.read_text(encoding="utf-8"))
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
