# evaluation

Offline quality measurement for embedding models.

**Owner**: Shared

## Modules

| File | Responsibility |
|------|---------------|
| `retrieval.py` | Recall@k, MRR, nDCG |
| `similarity.py` | Cosine similarity on STS benchmarks |
| `clustering.py` | V-measure, NMI on clustering tasks |
| `classification.py` | Linear probe accuracy |
| `mteb_runner.py` | Full MTEB benchmark suite |

## When to run

1. **During training** — validation pass every N steps (configured in `train.yaml`)
2. **After training** — full benchmark on best checkpoint
3. **Before deployment** — regression check vs previous best
4. **After CUDA changes** — verify kernel outputs match PyTorch reference

## Configuration

Reads `configs/eval.yaml`:

- Benchmark suites to run
- Batch size
- Metrics to report
- Output directory

## Output

Results written to `experiments/<run_id>/eval/`:

```
eval/
  retrieval.json
  similarity.json
  mteb/summary.csv
  plots/
```

## Usage

```bash
export PYTHONPATH=src
python -m evaluation.mteb_runner --config configs/eval.yaml --checkpoint experiments/run_001/checkpoints/best/
```

See `docs/Evaluation.md` for benchmark details.
