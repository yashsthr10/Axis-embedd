# model

Neural network architecture and building blocks. Model code only — no training or inference logic.

**Owner**: You

## Modules

| File | Responsibility |
|------|---------------|
| `embeddings.py` | Token and position embedding layers |
| `rope.py` | Rotary position embeddings |
| `rmsnorm.py` | Root mean square layer normalization |
| `swiglu.py` | SwiGLU feed-forward activation |
| `mla.py` | Multi-latent attention |
| `flash_attention.py` | Flash attention wrapper (PyTorch) |
| `encoder.py` | Stacked transformer encoder blocks |
| `tinyembed.py` | Top-level model: encoder + pooling + projection |

## Design rules

- Every module is a pure `nn.Module` with no side effects.
- Forward signature is consistent: `(input_ids, attention_mask) -> hidden_states`.
- `tinyembed.py` is the only public entry point; other modules are internal building blocks.
- PyTorch implementations only. CUDA optimizations live in `src/cuda/` and are swapped in at inference time.
- Architecture dimensions come from `configs/model.yaml`, never hardcoded.

## Interface

```python
# tinyembed.py
class TinyEmbed(nn.Module):
    def forward(self, input_ids, attention_mask) -> Tensor:
        # returns [batch, embed_dim]
        ...
```

## Dependencies

- Imports: PyTorch, `configs/model.yaml`
- Must not import: `training`, `inference`, `dataset`, `cuda` (sibling modules under `src/`)
