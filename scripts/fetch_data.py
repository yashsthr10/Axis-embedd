#!/usr/bin/env python3
"""Fetch raw text from Common Crawl into data/raw/."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from dataset.crawl.commoncrawl import CrawlConfig, fetch_commoncrawl
from dataset.paths import data_dir, resolve_repo_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch Common Crawl WET data")
    parser.add_argument("--crawl-id", default="CC-MAIN-2024-46")
    parser.add_argument("--num-wet-files", type=int, default=2)
    parser.add_argument("--max-records", type=int, default=5_000)
    parser.add_argument("--min-text-chars", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = resolve_repo_root(REPO_ROOT)
    raw_dir = data_dir(root) / "raw"

    config = CrawlConfig(
        crawl_id=args.crawl_id,
        num_wet_files=args.num_wet_files,
        max_records=args.max_records,
        min_text_chars=args.min_text_chars,
        seed=args.seed,
        output_jsonl=raw_dir / "documents.jsonl",
        manifest_path=raw_dir / "manifest.json",
    )

    result = fetch_commoncrawl(config)
    print(json.dumps(result.manifest, indent=2))
    print(f"\nSaved {result.records_written:,} records to {result.output_jsonl}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
