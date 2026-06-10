# Inference

Documentation for the serving and runtime layer.

## Overview

The inference module is the production face of tiny-embed. It loads a trained checkpoint, runs forward passes, and optionally serves embeddings over HTTP.

Think of it as a mini-vLLM for embeddings.

## Architecture

```
Request (text)
     |
     v
src/inference/server.py       HTTP/gRPC endpoint
     |
     v
src/inference/engine.py       Batch management, request queue
     |
     v
src/inference/loader.py       Load checkpoint + tokenizer
     |
     v
src/inference/runtime.py      Select PyTorch or CUDA backend
     |
     +---> PyTorch forward (src/model/)
     |
     +---> CUDA kernels (src/cuda/)
     |
     v
src/inference/quantization.py  Optional INT8/INT4 path
     |
     v
Response (embeddings)
```

## Module map

| File | Responsibility |
|------|---------------|
| `src/inference/engine.py` | Core inference orchestration |
| `src/inference/runtime.py` | Backend selection (PyTorch vs CUDA) |
| `src/inference/loader.py` | Checkpoint and tokenizer loading |
| `src/inference/quantization.py` | INT8/INT4 weight quantization |
| `src/inference/server.py` | HTTP API server |

## Configuration (`configs/inference.yaml`)

- `model_path`: Path to exported checkpoint
- `max_batch_size`: Maximum texts per batch
- `max_seq_length`: Truncation limit
- `device`: cuda / cpu
- `use_cuda_kernels`: true / false
- `quantization`: none / int8 / int4
- `server_port`: HTTP listen port

## API contract

```
POST /embed
Content-Type: application/json

{
  "texts": ["Hello world", "Another sentence"],
  "normalize": true
}

Response:
{
  "embeddings": [[0.1, 0.2, ...], [0.3, 0.4, ...]],
  "dim": 768,
  "model": "tiny-embed-v1"
}
```

## Performance targets

Track in `benchmarks/`:

- Latency (p50, p99) per request
- Throughput (queries/sec, tokens/sec)
- Memory footprint with and without quantization

## Owner

You own this module. See `src/inference/README.md`.
