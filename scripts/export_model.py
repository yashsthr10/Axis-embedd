#!/usr/bin/env python3
"""Export a training checkpoint for inference deployment."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export checkpoint for inference")
    parser.add_argument(
        "--checkpoint",
        type=Path,
        required=True,
        help="Path to checkpoint directory (e.g. experiments/run_001/checkpoints/best/)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("deployment/export"),
        help="Output directory for exported artifacts",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/model.yaml"),
        help="Model config to include in export",
    )
    return parser.parse_args()


def export(checkpoint: Path, output: Path, config: Path) -> None:
    if not checkpoint.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint}")

    output.mkdir(parents=True, exist_ok=True)

    for artifact in ("model.safetensors", "tokenizer.model", "tokenizer.json", "config.json"):
        src = checkpoint / artifact
        if src.exists():
            shutil.copy2(src, output / artifact)
            print(f"  copied {artifact}")
        else:
            print(f"  skipped {artifact} (not found)")

    if config.exists():
        shutil.copy2(config, output / "model.yaml")
        print("  copied model.yaml")

    print(f"Export complete: {output}")


def main() -> int:
    args = parse_args()
    try:
        export(args.checkpoint, args.output, args.config)
    except (FileNotFoundError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
