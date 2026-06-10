"""Text cleaning for raw web crawl data."""

from __future__ import annotations

import html
import re
import unicodedata

HTML_TAG_RE = re.compile(r"<[^>]+>")
CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
MULTI_SPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Remove HTML, control chars, broken whitespace, and normalize unicode."""
    text = html.unescape(text)
    text = HTML_TAG_RE.sub(" ", text)
    text = CONTROL_CHAR_RE.sub("", text)
    text = unicodedata.normalize("NFKC", text)
    text = MULTI_SPACE_RE.sub(" ", text)
    return text.strip()


def is_valid_text(text: str, min_chars: int = 50, min_words: int = 10) -> bool:
    """Reject empty or very short texts after cleaning."""
    return len(text) >= min_chars and len(text.split()) >= min_words
