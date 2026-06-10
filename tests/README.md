# tests

Unit and integration tests for every module.

**Owner**: Friend (setup), Shared (maintenance)

## Layout

```
tests/
  tokenizer/     Vocab coverage, encode/decode roundtrip
  dataset/         Pipeline stage output validation
  model/           Forward pass shapes, gradient flow
  training/        Loss computation, checkpoint roundtrip
  cuda/            Kernel correctness vs PyTorch reference
  inference/       API contract, batching, quantization
```

## Test categories

| Category | What to verify |
|----------|---------------|
| Unit | Individual functions and modules in isolation |
| Integration | Cross-module flows (dataset -> training -> eval) |
| Correctness | CUDA kernel output matches PyTorch within tolerance |
| Regression | Eval scores do not drop below recorded baseline |

## Running tests

```bash
# All tests
pytest tests/

# Single module
pytest tests/model/
pytest tests/cuda/

# With coverage
pytest tests/ --cov=model --cov=training --cov=inference
```

## Rules

- Tests must not require GPU unless in `tests/cuda/`.
- Tests must not download data — use fixtures in `tests/fixtures/`.
- CUDA correctness tests compare against `src/model/` PyTorch reference, not pre-computed golden values.
- Failing eval regression tests block deployment.
