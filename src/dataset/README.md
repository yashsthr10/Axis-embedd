# dataset

Data engineering pipeline: raw text to training-ready pairs.

**Owner**: Friend

## Pipeline

```
Raw Text
     |
     v
crawl/           Acquire raw text
     |
     v
clean/           Normalize, filter, strip markup
     |
     v
dedupe/          Remove exact and near-duplicates
     |
     v
preprocess/      Chunk, truncate, quality filter
     |
     v
pair_generation/ Create anchor/positive/negative triplets
     |
     v
builders/        Serialize to train/val/test splits
```

## Subfolders

| Folder | Input | Output |
|--------|-------|--------|
| `crawl/` | URLs, APIs, local files | Raw text in `data/raw/` |
| `clean/` | `data/raw/` | Cleaned text in `data/cleaned/` |
| `dedupe/` | `data/cleaned/` | Deduped text in `data/deduped/` |
| `preprocess/` | `data/deduped/` | Chunks in `data/processed/` |
| `pair_generation/` | `data/processed/` | Pairs in `data/pairs/` |
| `builders/` | `data/pairs/` | Final splits in `data/final/` |

## Output schema (TBD)

Define the canonical example format in `docs/Dataset.md` before building `builders/`.

## Notebook pattern

Data tasks follow **Notebook Driver + src Utility** (`docs/Patterns.md`):

| Notebook | src module | Output |
|----------|------------|--------|
| `notebooks/get_data.ipynb` | `crawl/commoncrawl.py` | `data/raw/` |
| `notebooks/preprocess_data.ipynb` | `clean/`, `dedupe/`, `preprocess/` | `data/cleaned/`, `data/deduped/` |

CLI equivalents: `make fetch`, `make preprocess`.

## Rules

- Each stage reads from the previous stage's output directory in `data/`.
- Stages must be independently runnable and resumable.
- No model or training code in this folder.
- Reusable logic lives in `src/dataset/` — notebooks only configure and visualize.
- Quality metrics (dedupe ratio, pair count, language distribution) logged per run.
