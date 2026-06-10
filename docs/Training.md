# Training

Documentation for the training loop and optimization.

## Overview

Training takes a model (from `src/model/`), a dataset (from `src/dataset/builders/`), and configuration (`configs/train.yaml`) and produces checkpoints.

## Training loop

```
1. Load config (train.yaml, model.yaml)
2. Initialize model, optimizer, scheduler
3. Build dataloader from `src/dataset/`
4. For each epoch:
     a. Forward pass (`src/model/`)
     b. Compute loss (`src/training/losses.py`)
     c. Backward pass
     d. Optimizer step (`src/training/optimizer.py`)
     e. Scheduler step (`src/training/scheduler.py`)
     f. Log metrics (`src/training/metrics.py`)
     g. Checkpoint if interval reached (`src/training/checkpoint.py`)
5. Final evaluation pass (`src/evaluation/`)
```

## Module map

| File | Responsibility |
|------|---------------|
| `src/training/trainer.py` | Main training loop, epoch management |
| `src/training/losses.py` | Contrastive, InfoNCE, triplet losses |
| `src/training/optimizer.py` | AdamW, Lion, or custom optimizer setup |
| `src/training/scheduler.py` | Cosine, warmup, linear decay |
| `src/training/checkpoint.py` | Save, load, resume from checkpoint |
| `src/training/metrics.py` | Loss curves, learning rate, throughput |

## Configuration (`configs/train.yaml`)

Key parameters (fill in when decided):

- `batch_size`
- `learning_rate`
- `num_epochs`
- `warmup_steps`
- `gradient_accumulation_steps`
- `checkpoint_interval`
- `eval_interval`
- `loss_type`
- `mixed_precision` (fp16 / bf16 / fp32)

## Checkpointing

Checkpoints are saved to `experiments/<run_id>/checkpoints/`:

```
checkpoints/
  step_1000/
    model.safetensors
    optimizer.pt
    scheduler.pt
    training_state.json
  step_2000/
    ...
  best/
    model.safetensors
```

## Resume

`src/training/checkpoint.py` must support:

- Resume from latest checkpoint in an experiment directory
- Resume from a specific step
- Load only model weights (for fine-tuning)

## Owner

You own this module. See `src/training/README.md`.
