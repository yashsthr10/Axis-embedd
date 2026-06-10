# Patterns

Document recurring implementation patterns to promote consistency.

## 1) Pattern template

- **Pattern name**:
- **When to use**:
- **When not to use**:
- **Structure**:
- **Example locations**:

## 2) Repository Pattern

- **Use for**: abstracting persistence from domain logic.
- **Benefits**: testability, swap-friendly storage adapters.

## 3) Service Pattern

- **Use for**: application-level orchestration of domain operations.
- **Benefits**: keeps handlers/controllers thin.

## 4) Event-Driven Pattern

- **Use for**: decoupled asynchronous processing.
- **Benefits**: scalability and isolation of side-effects.

## 5) Dependency Injection Pattern

- **Use for**: wiring interfaces/implementations cleanly.
- **Benefits**: easier testing and runtime composition.

## 6) Notebook Driver + src Utility Pattern

- **When to use**: data engineering, exploration, and pipeline stages where you want interactive execution with reusable logic.
- **When not to use**: production training loops, inference servers, or CUDA kernels — those belong in `src/` modules called by scripts/Makefile, not notebooks.
- **Structure**:

```
notebooks/<task>.ipynb     # thin driver: config, run, inspect results
        |
        v
src/<module>/              # reusable utilities and pipeline functions
        |
        v
data/<stage>/              # artifacts on disk
scripts/<task>.py          # optional CLI wrapper around the same src/ functions
```

- **Notebook responsibilities**:
  - Set config knobs (record limits, paths, thresholds).
  - Call `src/` functions.
  - Display summaries, samples, and plots.
  - Do not contain business logic that will be reused elsewhere.

- **src/ responsibilities**:
  - Implement fetch, clean, dedupe, inspect, and transform logic.
  - Expose typed config/result dataclasses (e.g. `CrawlConfig`, `PreprocessConfig`).
  - Be importable from notebooks, scripts, and tests.

- **Example locations**:
  - `notebooks/get_data.ipynb` -> `src/dataset/crawl/commoncrawl.py` -> `data/raw/`
  - `notebooks/preprocess_data.ipynb` -> `src/dataset/clean/`, `dedupe/`, `preprocess/` -> `data/cleaned/`, `data/deduped/`
  - `scripts/fetch_data.py`, `scripts/preprocess_data.py` — CLI entry points over the same utilities
  - `src/dataset/paths.py` — shared repo/data path resolution for notebooks and scripts

- **Guardrails**:
  - If logic appears in two notebooks, move it to `src/` immediately.
  - Notebooks may visualize; `src/` modules must not import matplotlib.
  - Scripts and notebooks should call the same `src/` functions — never fork logic.

## 7) Pattern guardrails

- Reuse existing patterns before introducing new abstractions.
- New patterns require an entry in `Decisions.md`.
