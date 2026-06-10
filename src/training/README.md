# training

Training loop, optimization, and checkpointing.

**Owner**: You

## Modules

| File | Responsibility |
|------|---------------|
| `trainer.py` | Main loop: forward, backward, epoch management |
| `losses.py` | Contrastive, InfoNCE, triplet objectives |
| `optimizer.py` | Optimizer setup (AdamW, etc.) |
| `scheduler.py` | Learning rate schedules (cosine, warmup) |
| `checkpoint.py` | Save, load, resume |
| `metrics.py` | Loss, LR, throughput logging |

## What lives here

- Forward and backward passes
- Loss computation and gradient updates
- Checkpoint save and resume
- Training-time metric collection
- Periodic validation calls into `evaluation`

## What does not live here

- Model architecture (import from `model`)
- Dataset building (import from `dataset.builders`)
- Benchmark suites (import from `evaluation`)

## Configuration

Reads `configs/train.yaml` and `configs/model.yaml` at startup.

## Checkpoints

Saved to `experiments/<run_id>/checkpoints/`:

```
step_<N>/
  model.safetensors
  optimizer.pt
  scheduler.pt
  training_state.json
```

## Usage

```bash
export PYTHONPATH=src
python -m training.trainer --config configs/train.yaml
python -m training.trainer --config configs/train.yaml --resume experiments/run_001/checkpoints/step_1000/
```

See `docs/Training.md` for the full training loop design.
