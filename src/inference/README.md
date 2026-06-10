# inference

Production serving layer — the mini-vLLM for embeddings.

**Owner**: You

## Modules

| File | Responsibility |
|------|---------------|
| `engine.py` | Core orchestration: batch, queue, dispatch |
| `runtime.py` | Backend selection (PyTorch vs CUDA kernels) |
| `loader.py` | Checkpoint and tokenizer loading |
| `quantization.py` | INT8/INT4 weight quantization |
| `server.py` | HTTP API endpoint |

## Architecture

```
POST /embed
     |
     v
server.py --> engine.py --> loader.py
                                |
                                v
                           runtime.py
                           /          \
                    PyTorch          CUDA (cuda/)
                           \          /
                                v
                         quantization.py (optional)
                                |
                                v
                         embeddings [batch, dim]
```

## Configuration

Reads `configs/inference.yaml`:

- `model_path`, `max_batch_size`, `max_seq_length`
- `device`, `use_cuda_kernels`, `quantization`
- `server_port`

## API

```
POST /embed
{ "texts": ["..."], "normalize": true }

-> { "embeddings": [[...]], "dim": 768, "model": "tiny-embed-v1" }
```

## Rules

- Inference code imports from `model` but never from `training`.
- CUDA kernels are opt-in via `use_cuda_kernels` in config.
- PyTorch fallback must always work without CUDA kernels installed.

See `docs/Inference.md` for full API and performance targets.
