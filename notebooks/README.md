# notebooks

Interactive drivers for data engineering and exploration.

## Pattern: Notebook Driver + src Utility

Notebooks orchestrate; `src/` implements. See `docs/Patterns.md` section 6.

```
notebook (config + run + visualize)
    -> src/dataset/ (reusable logic)
    -> data/ (artifacts)
```

**Notebooks own:** parameters, execution order, inspection, plots.
**src/ owns:** fetch, clean, dedupe, transform, and pipeline functions.
**scripts/ owns:** non-interactive CLI wrappers over the same `src/` code.

## Rules

- Keep notebooks thin. If logic is reused or exceeds ~30 lines, move it to `src/`.
- Do not commit large notebook outputs — clear outputs before committing.
- Reference data by path (`data/`, `experiments/<run_id>/`), never embed results inline.
- Use the `Python (tiny-embed)` kernel (project `.venv`).

## Notebooks

| Notebook | src modules | Output |
|----------|-------------|--------|
| `get_data.ipynb` | `dataset/crawl/commoncrawl.py` | `data/raw/documents.jsonl` |
| `preprocess_data.ipynb` | `dataset/clean/`, `dedupe/`, `preprocess/` | `data/cleaned/`, `data/deduped/`, `data/processed/` |

## CLI equivalents

```bash
make fetch        # same logic as get_data.ipynb
make preprocess   # same logic as preprocess_data.ipynb
```
