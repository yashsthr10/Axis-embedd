# Structure

Defines where code should go and how directories are organized.

## 1) Top-level layout

- `src/` - all Python source code.
- `tests/` - unit, integration, and correctness tests.
- `scripts/` - development and operational scripts.
- `docs/` - repository knowledge and design documents.
- `configs/` - static configuration templates (model, train, eval, inference).
- `data/` - raw and intermediate data artifacts (gitignored).
- `benchmarks/` - latency, throughput, memory, retrieval measurements.
- `experiments/` - per-run configs, checkpoints, results, notes.
- `notebooks/` - exploratory analysis.
- `deployment/` - packaging and serving infrastructure.

## 2) Source layout (`src/`)

- `src/model/` - encoder architecture and building blocks.
- `src/training/` - training loop, losses, optimizer, checkpoints.
- `src/evaluation/` - retrieval, similarity, clustering, MTEB.
- `src/inference/` - runtime engine, quantization, server.
- `src/cuda/` - custom GPU kernels (inference-only).
- `src/tokenizer/` - vocabulary training and export.
- `src/dataset/` - crawl, clean, dedupe, preprocess, pair generation.

## 3) Placement rules

- Model code belongs in `src/model/`. No training or inference logic.
- Training code belongs in `src/training/`. No model architecture definitions.
- CUDA kernels belong in `src/cuda/`. Never merged into `src/model/`.
- Data processing logic belongs in `src/dataset/`. Artifacts go in `data/`.
- All hyperparameters live in `configs/`. No hardcoded values in source.
- Cross-module imports follow pipeline direction: `dataset` -> `training` -> `evaluation` / `inference`.

## 4) Python path

Run modules from the repository root with `src/` on the path:

```bash
export PYTHONPATH=src
python -m training.trainer --config configs/train.yaml
```

## 5) Ownership

Module ownership and boundaries are in `Modules.md`.
