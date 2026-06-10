# deployment

Packaging, containerization, and serving infrastructure.

## Layout

```
deployment/
  Dockerfile           Container image for inference server
  docker-compose.yaml  Local dev stack (server + optional monitoring)
  export/              Exported model artifacts ready to serve
  k8s/                 Kubernetes manifests (optional, add when needed)
```

## Quick start

```bash
make export CHECKPOINT=experiments/experiment_001/checkpoints/best
make docker-build
make docker-up
curl http://localhost:8000/health
```

## Deployment flow

```
experiments/<run_id>/checkpoints/best/
     |
     v
scripts/export_model.py
     |
     v
deployment/export/
  model.safetensors
  config.json
  tokenizer.model
     |
     v
docker build -f deployment/Dockerfile .
     |
     v
src/inference/server.py  (serves POST /embed)
```

## Configuration

Inference runtime reads `configs/inference.yaml`. For deployment, override via environment variables:

| Env var | Config key |
|---------|-----------|
| `TINYEMBED_MODEL_PATH` | `model_path` |
| `TINYEMBED_PORT` | `server_port` |
| `TINYEMBED_QUANTIZATION` | `quantization` |
| `TINYEMBED_CUDA_KERNELS` | `use_cuda_kernels` |

## Health check

```
GET /health
-> { "status": "ok", "model": "tiny-embed-v1", "device": "cuda:0" }
```

## Rules

- `deployment/export/` contains only the artifacts needed to serve — no training state.
- Docker image runs `src/inference/server.py`, not the training loop.
- Pin dependency versions in the Dockerfile for reproducible builds.
