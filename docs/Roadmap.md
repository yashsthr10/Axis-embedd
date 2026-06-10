# Roadmap

Phased plan for building tiny-embed from scratch.

## Phase 1: Foundation (current)

- [x] Repository structure and documentation
- [ ] Config schema (`configs/*.yaml`)
- [ ] Tokenizer training pipeline
- [ ] Dataset crawl and clean pipeline
- [ ] Basic encoder model (PyTorch only)

## Phase 2: Training

- [ ] Contrastive training loop
- [ ] Checkpoint save/resume
- [ ] Validation evaluation during training
- [ ] First end-to-end training run
- [ ] Experiment tracking in `experiments/`

## Phase 3: Evaluation

- [ ] Retrieval and similarity benchmarks
- [ ] MTEB integration
- [ ] Baseline score recording
- [ ] Regression test suite

## Phase 4: Inference

- [ ] Model export and loading
- [ ] Batch inference engine
- [ ] HTTP server
- [ ] Latency and throughput benchmarks

## Phase 5: CUDA optimization

- [ ] RMSNorm kernel
- [ ] Flash attention kernel
- [ ] MLA kernel
- [ ] SwiGLU kernel
- [ ] Pooling kernel
- [ ] INT8/INT4 quantization kernels
- [ ] Kernel correctness tests (match PyTorch reference)

## Phase 6: Production

- [ ] Deployment packaging
- [ ] CI/CD for training and inference
- [ ] Model versioning
- [ ] Monitoring and observability

## Milestones

| Milestone | Target | Success criteria |
|-----------|--------|-----------------|
| M1: First tokenizer | TBD | `tokenizer.model` trains on corpus |
| M2: First dataset | TBD | Training pairs in `data/final/` |
| M3: First model | TBD | Forward pass produces `[batch, dim]` |
| M4: First training run | TBD | Loss decreases over 1 epoch |
| M5: First eval scores | TBD | MTEB scores recorded in `experiments/` |
| M6: First inference | TBD | `/embed` endpoint returns embeddings |
| M7: CUDA speedup | TBD | 2x throughput vs PyTorch baseline |
