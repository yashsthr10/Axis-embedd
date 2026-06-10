# tiny-embed

End-to-end repository for building a text embedding model from scratch.

## Pipeline

```
Raw Text
     |
     v
Tokenizer
     |
     v
Dataset
     |
     v
Training
     |
     v
Embedding Model
     |
     v
Evaluation
     |
     v
CUDA Inference
```

## Layout

| Path | Purpose | Owner |
|------|---------|-------|
| `docs/` | Architecture, design, decisions, roadmap | Friend |
| `configs/` | All hyperparameters and runtime settings | Shared |
| `data/` | Raw and intermediate data artifacts | Shared |
| `src/tokenizer/` | Vocabulary training and export | Friend |
| `src/dataset/` | Crawl, clean, dedupe, preprocess, pair generation | Friend |
| `src/model/` | Encoder architecture and building blocks | You |
| `src/training/` | Trainer, losses, optimizer, checkpoints | You |
| `src/evaluation/` | Retrieval, similarity, MTEB benchmarks | Shared |
| `src/inference/` | Runtime engine, quantization, server | You |
| `src/cuda/` | Custom GPU kernels | You |
| `scripts/` | One-off and operational scripts | Shared |
| `tests/` | Unit and integration tests | Friend |
| `benchmarks/` | Latency, throughput, memory, retrieval | Shared |
| `experiments/` | Per-run configs, results, notes | Shared |
| `notebooks/` | Exploratory analysis | Shared |
| `deployment/` | Packaging and serving infrastructure | Shared |

## Getting started

1. Read `docs/Architecture.md` for the full system design.
2. Read `docs/Decisions.md` before making major technical choices.
3. Bootstrap the environment:

```bash
./scripts/setup_env.sh
# or
make setup
```

4. Copy and adjust environment variables:

```bash
cp .env.example .env
```

## Makefile

```bash
make help          # list all targets
make setup         # create venv and install deps
make train         # run training
make eval          # run evaluation
make infer         # start inference server
make export        # export checkpoint for deployment
make test          # run tests
make lint          # ruff lint
make check         # lint + typecheck + test
make docker-build  # build inference image
make docker-up     # start server via docker compose
```

Override defaults via env vars or Make arguments:

```bash
make train EXPERIMENT=experiment_002 TRAIN_CONFIG=configs/train.yaml
make eval CHECKPOINT=experiments/experiment_002/checkpoints/best
```

## Rules

- Model code lives in `src/model/`. No training logic there.
- Training code lives in `src/training/`. No model architecture there.
- Every major choice (MLA vs MHA, SentencePiece vs BPE, INT8 vs INT4) goes in `docs/Decisions.md`.
- Experiment results never leave `experiments/` — configs, graphs, and notes stay together.
