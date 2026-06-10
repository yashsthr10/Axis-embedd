"""Common Crawl WET fetch utilities."""

from __future__ import annotations

import gzip
import hashlib
import json
import random
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any

import requests
from tqdm.auto import tqdm
from warcio.archiveiterator import ArchiveIterator

CC_BASE_URL = "https://data.commoncrawl.org"
CC_INDEX_URL = "https://index.commoncrawl.org/collinfo.json"


@dataclass
class CrawlConfig:
    crawl_id: str
    num_wet_files: int = 2
    max_records: int = 5_000
    min_text_chars: int = 200
    seed: int = 42
    output_jsonl: Path = field(default_factory=lambda: Path("data/raw/documents.jsonl"))
    manifest_path: Path = field(default_factory=lambda: Path("data/raw/manifest.json"))


@dataclass
class CrawlResult:
    records_written: int
    wet_files_used: list[str]
    crawl_info: dict[str, Any]
    manifest: dict[str, Any]
    output_jsonl: Path
    manifest_path: Path


def fetch_json(url: str, timeout: int = 30) -> list[dict[str, Any]] | dict[str, Any]:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()


def list_available_crawls() -> list[dict[str, Any]]:
    crawls = fetch_json(CC_INDEX_URL)
    return sorted(crawls, key=lambda c: c["id"], reverse=True)


def pick_crawl(crawl_id: str | None = None) -> dict[str, Any]:
    crawls = list_available_crawls()
    if crawl_id:
        match = next((c for c in crawls if c["id"] == crawl_id), None)
        if match is None:
            known = [c["id"] for c in crawls[:5]]
            raise ValueError(f"Unknown crawl {crawl_id!r}. Recent crawls: {known}")
        return match
    return crawls[0]


def load_wet_paths(crawl_id: str) -> list[str]:
    url = f"{CC_BASE_URL}/crawl-data/{crawl_id}/wet.paths.gz"
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    with gzip.open(BytesIO(response.content), "rt", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip()]


def select_wet_paths(crawl_id: str, num_files: int, seed: int) -> list[str]:
    wet_paths = load_wet_paths(crawl_id)
    rng = random.Random(seed)
    return rng.sample(wet_paths, k=min(num_files, len(wet_paths)))


def record_id(url: str, wet_path: str, warc_record_id: str) -> str:
    payload = f"{url}|{wet_path}|{warc_record_id}"
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def iter_wet_records_from_url(
    wet_url: str,
    wet_path: str,
    crawl_id: str,
    min_text_chars: int,
    chunk_size: int = 1024 * 1024,
) -> Iterator[dict[str, Any]]:
    """Stream a WET file from Common Crawl and parse in memory (no disk cache)."""
    with requests.get(wet_url, stream=True, timeout=300) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))

        with tempfile.SpooledTemporaryFile(max_size=64 * 1024 * 1024) as tmp:
            with tqdm(total=total, unit="B", unit_scale=True, desc=Path(wet_path).name) as bar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        tmp.write(chunk)
                        bar.update(len(chunk))
            tmp.seek(0)

            with gzip.open(tmp, "rb") as stream:
                for record in ArchiveIterator(stream):
                    if record.rec_type != "conversion":
                        continue

                    url = record.rec_headers.get_header("WARC-Target-URI")
                    warc_record_id = record.rec_headers.get_header("WARC-Record-ID")
                    text = record.content_stream().read().decode("utf-8", errors="replace").strip()
                    if len(text) < min_text_chars:
                        continue

                    yield {
                        "id": record_id(url, wet_path, warc_record_id),
                        "warc_record_id": warc_record_id,
                        "url": url,
                        "crawl_id": crawl_id,
                        "wet_file": wet_path,
                        "text": text,
                        "char_count": len(text),
                    }


def fetch_commoncrawl(config: CrawlConfig) -> CrawlResult:
    """Download and parse Common Crawl WET records into JSONL."""
    crawl_info = pick_crawl(config.crawl_id)
    crawl_id = crawl_info["id"]
    selected_paths = select_wet_paths(crawl_id, config.num_wet_files, config.seed)

    config.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    config.manifest_path.parent.mkdir(parents=True, exist_ok=True)

    records_written = 0
    wet_files_used: list[str] = []

    with open(config.output_jsonl, "w", encoding="utf-8") as out_fh:
        for wet_path in selected_paths:
            if records_written >= config.max_records:
                break

            wet_files_used.append(wet_path)
            wet_url = f"{CC_BASE_URL}/{wet_path}"
            for doc in iter_wet_records_from_url(
                wet_url, wet_path, crawl_id, config.min_text_chars
            ):
                out_fh.write(json.dumps(doc, ensure_ascii=False) + "\n")
                records_written += 1
                if records_written >= config.max_records:
                    break

    manifest = {
        "source": "commoncrawl",
        "crawl_id": crawl_id,
        "crawl_name": crawl_info.get("name"),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "wet_files_requested": config.num_wet_files,
        "wet_files_used": wet_files_used,
        "max_records": config.max_records,
        "records_written": records_written,
        "min_text_chars": config.min_text_chars,
        "output_file": str(config.output_jsonl),
        "format": "jsonl",
        "fields": [
            "id",
            "warc_record_id",
            "url",
            "crawl_id",
            "wet_file",
            "text",
            "char_count",
        ],
        "license": "https://commoncrawl.org/terms-of-use",
    }

    with open(config.manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)

    return CrawlResult(
        records_written=records_written,
        wet_files_used=wet_files_used,
        crawl_info=crawl_info,
        manifest=manifest,
        output_jsonl=config.output_jsonl,
        manifest_path=config.manifest_path,
    )
