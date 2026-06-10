"""Shared path helpers for dataset notebooks and scripts."""

from __future__ import annotations

from pathlib import Path


def resolve_repo_root(start: Path | None = None) -> Path:
    """Resolve repository root from a notebook, script, or cwd."""
    current = (start or Path.cwd()).resolve()
    if current.name == "notebooks":
        return current.parent
    if (current / "data" / "raw").exists() or (current / "src" / "dataset").exists():
        return current
    if (current.parent / "data" / "raw").exists():
        return current.parent
    return current


def data_dir(repo_root: Path | None = None) -> Path:
    return resolve_repo_root(repo_root) / "data"
