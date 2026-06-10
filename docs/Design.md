# Design

Principles and design approach for tiny-embed.

## Goals

- Build a competitive text embedding model from scratch.
- Keep data engineering, model code, training, and inference cleanly separated.
- Support custom CUDA kernels without coupling them to model architecture.
- Make every experiment reproducible and every decision traceable.

## Design principles

### 1. Separation of concerns

Each `src/` module owns exactly one phase of the pipeline. Cross-module imports follow the data flow direction: `dataset` -> `training` -> `evaluation` / `inference`. `src/model/` is imported by `src/training/` and `src/inference/` but never the reverse.

### 2. Configuration over code

Hyperparameters, paths, and runtime settings live in `configs/*.yaml`. Code reads config at startup. Changing a learning rate never requires a code change.

### 3. PyTorch first, CUDA second

Every operation in `src/model/` has a pure PyTorch implementation. CUDA kernels in `src/cuda/` are drop-in replacements optimized for inference. Training always uses PyTorch; inference can opt into CUDA.

### 4. Fail loud, log everything

Training metrics, evaluation scores, and benchmark results are written to disk in structured format. Silent failures are not acceptable.

### 5. Document before you build

Major architectural choices go into `Decisions.md` before implementation begins. The cost of a wrong abstraction is higher than the cost of a short design discussion.

## Model design (placeholder)

Fill in as decisions are made:

- **Architecture**: Encoder-only transformer (details TBD)
- **Attention**: TBD (MLA vs MHA — see `Decisions.md`)
- **Pooling**: TBD (mean, CLS, last-token)
- **Loss**: TBD (contrastive, InfoNCE, triplet)
- **Tokenizer**: TBD (SentencePiece vs BPE — see `Decisions.md`)

## Interface contracts

### Model output

The encoder produces a fixed-dimensional embedding vector per input sequence:

```
input_ids:  [batch, seq_len]
attention_mask: [batch, seq_len]
--> embeddings: [batch, embed_dim]
```

### Checkpoint format

```
checkpoint/
  model.safetensors
  config.json
  tokenizer.model
  training_state.pt  (optional, for resume)
```

### Inference API

```
POST /embed
  body: { "texts": ["...", "..."] }
  response: { "embeddings": [[...], [...]], "dim": 768 }
```

## What not to do

- Do not put training loops in `src/model/`.
- Do not hardcode paths or hyperparameters in Python files.
- Do not store experiment results outside `experiments/`.
- Do not merge CUDA kernel code into `src/model/` — keep it in `src/cuda/`.
