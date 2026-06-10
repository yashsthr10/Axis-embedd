# cuda

Custom GPU kernels for optimized inference. PyTorch reference implementations stay in `src/model/`.

**Owner**: You

## Layout

```
src/cuda/
  rmsnorm/           RMSNorm kernel
  flash_attention/   Flash attention kernel
  mla/               Multi-latent attention kernel
  swiglu/            SwiGLU FFN kernel
  pooling/           Mean/CLS pooling kernel
  quantization/      INT8/INT4 quantization kernels
```

## Per-kernel structure

Each subfolder follows this pattern:

```
src/cuda/flash_attention/
  kernel.cu            CUDA kernel implementation
  launcher.cpp         C++ launcher binding
  __init__.py          Python wrapper with PyTorch fallback
  test_correctness.py  Verify output matches src/model/ reference
```

## Integration

Kernels are swapped in at inference time via `src/inference/runtime.py`:

```python
if config.use_cuda_kernels:
    from cuda.flash_attention import flash_attention_cuda
else:
    from model.flash_attention import flash_attention_pytorch
```

Requires `PYTHONPATH=src` when running from the repository root.

## Development order

1. PyTorch reference in `src/model/` (must exist first)
2. Correctness test in `tests/cuda/` comparing CUDA vs PyTorch
3. Benchmark in `benchmarks/latency/` and `benchmarks/throughput/`
4. Enable in `src/inference/runtime.py`

## Rules

- Training always uses PyTorch. CUDA kernels are inference-only.
- Every kernel must have a correctness test that matches the `src/model/` reference within tolerance.
- Kernel code never imports from `training` or `dataset`.
