# Evaluation

Documentation for offline quality measurement.

## Purpose

Measure how good the embedding model is before and after deployment. Evaluation runs on held-out data and standard benchmarks.

## Evaluation suites

| Module | What it measures |
|--------|-----------------|
| `src/evaluation/retrieval.py` | Recall@k, MRR, nDCG on retrieval tasks |
| `src/evaluation/similarity.py` | Cosine similarity on STS benchmarks |
| `src/evaluation/clustering.py` | V-measure, NMI on clustering tasks |
| `src/evaluation/classification.py` | Linear probe accuracy on classification tasks |
| `src/evaluation/mteb_runner.py` | Full MTEB benchmark suite runner |

## When to evaluate

1. **During training**: Validation pass every N steps (configured in `train.yaml`).
2. **After training**: Full benchmark suite on best checkpoint.
3. **Before deployment**: Regression check against previous best model.
4. **After CUDA optimization**: Verify kernel outputs match PyTorch reference.

## Configuration (`configs/eval.yaml`)

- Benchmark suites to run
- Batch size for evaluation
- Metrics to report
- Output directory for results

## Output format

Results are written to `experiments/<run_id>/eval/`:

```
eval/
  retrieval.json
  similarity.json
  mteb/
    summary.csv
    per_task/
  plots/
    recall_at_k.png
```

## MTEB integration

`mteb_runner.py` wraps the MTEB library:

```
checkpoint + config --> mteb_runner --> leaderboard scores
```

Record baseline and target scores in `experiments/` notes.

## Owner

Shared between training and inference teams.
