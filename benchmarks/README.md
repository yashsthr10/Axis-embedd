# benchmarks

Performance measurement for training and inference.

**Owner**: Shared

## Layout

```
benchmarks/
  latency/       Per-request and per-batch latency (p50, p99)
  throughput/    Tokens/sec, queries/sec under load
  memory/        Peak GPU/CPU memory at various batch sizes
  retrieval/     Quality vs speed tradeoff curves
```

## Metrics to track

| Metric | Unit | Where measured |
|--------|------|---------------|
| Training throughput | tokens/sec | `src/training/` |
| Inference latency | ms (p50, p99) | `src/inference/` |
| Inference throughput | queries/sec | `src/inference/` |
| GPU memory | MB / GB | `src/inference/`, `src/cuda/` |
| Retrieval quality | Recall@k | `src/evaluation/` |

## Output

Results stored in `experiments/<run_id>/benchmarks/`:

```
benchmarks/
  latency/
    pytorch_baseline.json
    cuda_optimized.json
  throughput/
    batch_1.json
    batch_32.json
  memory/
    fp16.json
    int8.json
  retrieval/
    quality_vs_latency.csv
```

## Usage

```bash
python benchmarks/latency/run.py --config configs/inference.yaml
python benchmarks/throughput/run.py --config configs/inference.yaml --batch-sizes 1,8,32,64
```

## Rules

- Always benchmark PyTorch baseline before CUDA optimized version.
- Record hardware info (GPU model, driver version, CUDA version) with every result.
- Compare against previous experiment results to detect regressions.
