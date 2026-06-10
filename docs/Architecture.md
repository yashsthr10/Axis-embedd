# Architecture

System design for tiny-embed: a from-scratch text embedding model.

## System overview

tiny-embed is a modular pipeline that transforms raw text into a production-ready embedding model with custom CUDA inference.

```
                         DATA ENGINEERING
+------------------------------------------------------------------+
|                                                                  |
|  Raw Text --> Crawl --> Clean --> Dedupe --> Preprocess          |
|                                    |                             |
|                                    v                             |
|                              Pair Generation                     |
|                                    |                             |
|                                    v                             |
|                              Dataset Builders                    |
|                                                                  |
+------------------------------------------------------------------+
                                    |
                                    v
                              Tokenizer
                         (SentencePiece / BPE)
                                    |
                                    v
+------------------------------------------------------------------+
|                         MODEL DEVELOPMENT                        |
|                                                                  |
|  embeddings.py  rope.py  rmsnorm.py  swiglu.py                 |
|  mla.py  flash_attention.py  encoder.py  tinyembed.py            |
|                                                                  |
+------------------------------------------------------------------+
                                    |
                                    v
+------------------------------------------------------------------+
|                            TRAINING                              |
|                                                                  |
|  trainer.py  losses.py  optimizer.py  scheduler.py               |
|  checkpoint.py  metrics.py                                       |
|                                                                  |
+------------------------------------------------------------------+
                                    |
                                    v
                         Embedding Model
                          (checkpoint)
                                    |
                    +---------------+---------------+
                    |                               |
                    v                               v
+----------------------------+    +----------------------------+
|        EVALUATION          |    |         INFERENCE          |
|                            |    |                            |
|  retrieval  similarity     |    |  engine  runtime  loader   |
|  clustering  classification|    |  quantization  server      |
|  mteb_runner               |    |                            |
+----------------------------+    +----------------------------+
                    |                               |
                    v                               v
              Benchmarks                      CUDA Kernels
           (latency, throughput,          (rmsnorm, flash_attention,
            memory, retrieval)              mla, swiglu, pooling,
                                            quantization)
```

## Component boundaries

### Data Engineering (`src/dataset/`, `src/tokenizer/`, `data/`)

- **Input**: Raw text corpora, web crawls, curated datasets.
- **Output**: Tokenized training pairs ready for the dataloader.
- **Owns**: Crawling, cleaning, deduplication, preprocessing, pair generation, vocabulary training.
- **Must not**: Contain model architecture or training loop code.

### Model Development (`src/model/`)

- **Input**: Configuration from `configs/model.yaml`.
- **Output**: A `nn.Module` graph (encoder + pooling + projection).
- **Owns**: All neural network building blocks.
- **Must not**: Contain training, data loading, or inference serving code.

### Training (`src/training/`)

- **Input**: Model, dataset, config from `configs/train.yaml`.
- **Output**: Checkpoints, training metrics, logs.
- **Owns**: Forward/backward loop, loss computation, optimizer, scheduler, checkpointing.
- **Must not**: Define model architecture (imports from `src/model/`).

### Evaluation (`src/evaluation/`)

- **Input**: Trained checkpoint, benchmark datasets.
- **Output**: Retrieval scores, similarity metrics, MTEB leaderboard entries.
- **Owns**: All offline quality measurement.
- **Shared**: Used during training (validation) and after training (final eval).

### Inference (`src/inference/`)

- **Input**: Exported checkpoint, `configs/inference.yaml`.
- **Output**: Embeddings for arbitrary text input.
- **Owns**: Model loading, runtime execution, quantization, HTTP/gRPC server.
- **Becomes**: The mini-vLLM serving layer.

### CUDA Kernels (`src/cuda/`)

- **Input**: PyTorch reference implementations from `src/model/`.
- **Output**: Custom `.cu` kernels with Python launchers.
- **Owns**: GPU-optimized versions of rmsnorm, flash attention, MLA, SwiGLU, pooling, quantization.
- **Integration**: Swapped in at inference time via `src/inference/runtime.py`.

## Data flow

```
Raw Text
     |
     v
[ src/dataset/crawl ] --> [ src/dataset/clean ] --> [ src/dataset/dedupe ]
     |
     v
[ src/dataset/preprocess ] --> [ src/dataset/pair_generation ]
     |
     v
[ src/dataset/builders ] --> Training Dataset (on disk in data/final/)
     |
     v
[ src/tokenizer/ ] --> tokenizer.model, tokenizer.json
     |
     v
[ src/training/trainer.py ] <-- configs/train.yaml
     |                            configs/model.yaml
     v
Checkpoint (.pt / .safetensors)
     |
     +---> [ src/evaluation/ ] --> metrics, MTEB scores
     |
     +---> [ src/inference/engine.py ] --> embeddings
              |
              v
           [ src/cuda/ kernels ] --> optimized inference
```

## Configuration model

All runtime values live in `configs/`:

| File | Governs |
|------|---------|
| `model.yaml` | Architecture dimensions, layer count, attention type |
| `tokenizer.yaml` | Vocab size, algorithm, special tokens |
| `train.yaml` | Batch size, LR, epochs, loss type, checkpoint interval |
| `eval.yaml` | Benchmark suites, batch size, metrics to report |
| `inference.yaml` | Quantization, batching, server port, max sequence length |

No hardcoded values in source code. Ever.

## Non-functional requirements

- **Reproducibility**: Every experiment directory stores its config snapshot.
- **Modularity**: Each folder has a single responsibility and a README.
- **Traceability**: Major decisions recorded in `Decisions.md` with date and rationale.
- **Performance**: CUDA kernels are optional accelerators; PyTorch fallbacks always exist.

## References

- Design principles: `Design.md`
- Dataset pipeline: `Dataset.md`
- Training loop: `Training.md`
- Evaluation suites: `Evaluation.md`
- Serving layer: `Inference.md`
- Decision log: `Decisions.md`
- Future work: `Roadmap.md`
