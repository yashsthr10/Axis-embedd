# Modules

High-level map of codebase modules and ownership.

## 1) Module catalog

| Module | Path | Purpose | Owner |
|--------|------|---------|-------|
| Model | `src/model/` | Encoder architecture and building blocks | You |
| Training | `src/training/` | Training loop, losses, optimizer, checkpoints | You |
| Evaluation | `src/evaluation/` | Retrieval, similarity, MTEB benchmarks | Shared |
| Inference | `src/inference/` | Runtime engine, quantization, HTTP server | You |
| CUDA | `src/cuda/` | Custom GPU kernels for inference | You |
| Tokenizer | `src/tokenizer/` | Vocabulary training and export | Friend |
| Dataset | `src/dataset/` | Data engineering pipeline | Friend |

## 2) Non-source modules

| Module | Path | Purpose | Owner |
|--------|------|---------|-------|
| Configs | `configs/` | All hyperparameters and runtime settings | Shared |
| Data | `data/` | Raw and intermediate data artifacts | Shared |
| Scripts | `scripts/` | One-off operational scripts | Shared |
| Tests | `tests/` | Unit and integration tests | Friend |
| Benchmarks | `benchmarks/` | Performance measurement | Shared |
| Experiments | `experiments/` | Per-run artifacts and notes | Shared |
| Notebooks | `notebooks/` | Exploratory analysis | Shared |
| Deployment | `deployment/` | Containerization and serving | Shared |

## 3) Dependency direction

```
src/dataset/  -->  src/training/  -->  src/evaluation/
                        |                    |
                        v                    v
                  src/model/  <------  src/inference/  <--  src/cuda/
                        ^
                        |
                  src/tokenizer/
```

- `src/model/` is imported by `src/training/` and `src/inference/`.
- `src/cuda/` is imported only by `src/inference/`.
- `src/dataset/` and `src/tokenizer/` are imported by `src/training/`.
- No reverse imports (e.g. `src/model/` must not import `src/training/`).

## 4) Ownership rules

- Each module has a clear owner.
- Cross-module writes require explicit contracts.
- Major decisions go in `docs/Decisions.md` before implementation.
