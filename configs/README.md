# configs

All configurable values for tiny-embed. No hardcoded hyperparameters in source code.

## Files

| File | Governs |
|------|---------|
| `model.yaml` | Architecture: layers, hidden dim, attention type, pooling |
| `tokenizer.yaml` | Vocab size, algorithm, special tokens, training corpus path |
| `train.yaml` | Batch size, LR, epochs, loss, checkpoint interval |
| `eval.yaml` | Benchmark suites, metrics, evaluation batch size |
| `inference.yaml` | Quantization, batching, server port, max sequence length |

## Rules

- Code reads config at startup; never embed magic numbers in Python.
- Experiment runs copy the active config into `experiments/<run_id>/configs/`.
- Config changes that affect model behavior must be noted in `docs/Decisions.md`.

## Usage

```bash
export PYTHONPATH=src

# Training
python -m training.trainer --config configs/train.yaml

# Evaluation
python -m evaluation.mteb_runner --config configs/eval.yaml

# Inference
python -m inference.server --config configs/inference.yaml
```
