# Dataset

Documentation for the data engineering pipeline.

## Pipeline stages

```
Raw Text
     |
     v
crawl/        Acquire raw text from sources
     |
     v
clean/        Remove HTML, normalize whitespace, filter language
     |
     v
dedupe/       Remove exact and near-duplicate documents
     |
     v
preprocess/   Chunk, truncate, filter by quality heuristics
     |
     v
pair_generation/   Create positive/negative pairs for contrastive training
     |
     v
builders/     Serialize to training-ready format (JSONL, Arrow, etc.)
```

## Directory map

| Subfolder | Responsibility |
|-----------|---------------|
| `src/dataset/crawl/` | Download and ingest raw corpora |
| `src/dataset/clean/` | Text normalization and filtering |
| `src/dataset/dedupe/` | MinHash, SimHash, or exact-hash deduplication |
| `src/dataset/preprocess/` | Chunking, token-count filtering, quality scoring |
| `src/dataset/pair_generation/` | Hard negative mining, in-batch negatives |
| `src/dataset/builders/` | Final dataset serialization and train/val/test splits |

## Data storage

Raw and intermediate artifacts live in `data/`:

```
data/
  raw/           Original downloads (never modify)
  cleaned/       Post-cleaning output
  deduped/       Post-deduplication output
  processed/     Chunked and filtered text
  pairs/         Training pairs
  final/         Train/val/test splits ready for training
```

## Output format (TBD)

Define the canonical training example schema here once decided:

```json
{
  "anchor": "string",
  "positive": "string",
  "negative": "string | null",
  "source": "string",
  "metadata": {}
}
```

## Quality gates

- Minimum token count per document
- Maximum duplicate ratio after dedupe
- Language detection confidence threshold
- Train/val/test leakage checks

## Owner

Friend owns this pipeline. See `src/dataset/README.md` for implementation details.
