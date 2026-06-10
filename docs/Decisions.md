# Decisions

Major technical decisions and their rationale. Future you will thank present you.

## Format

Each entry follows this template:

```
### DEC-NNN: Title
- **Date**: YYYY-MM-DD
- **Status**: proposed | accepted | rejected | superseded
- **Context**: What problem are we solving?
- **Decision**: What did we choose?
- **Alternatives**: What else was considered?
- **Rationale**: Why this choice?
- **Consequences**: What does this commit us to?
```

---

## Pending decisions

Record choices here as they are made:

### DEC-001: Attention mechanism (MLA vs MHA)
- **Date**: TBD
- **Status**: proposed
- **Context**: Choose the attention implementation for the encoder.
- **Alternatives**: Multi-head attention (MHA), Multi-latent attention (MLA)
- **Decision**: TBD

### DEC-002: Tokenizer algorithm (SentencePiece vs BPE)
- **Date**: TBD
- **Status**: proposed
- **Context**: Choose the subword tokenization algorithm.
- **Alternatives**: SentencePiece (unigram/BPE), HuggingFace BPE, WordPiece
- **Decision**: TBD

### DEC-003: Inference quantization (INT8 vs INT4)
- **Date**: TBD
- **Status**: proposed
- **Context**: Choose quantization strategy for production inference.
- **Alternatives**: FP16, INT8, INT4, none
- **Decision**: TBD

### DEC-004: Training loss function
- **Date**: TBD
- **Status**: proposed
- **Context**: Choose the contrastive learning objective.
- **Alternatives**: InfoNCE, triplet loss, multiple negatives ranking
- **Decision**: TBD

### DEC-005: Pooling strategy
- **Date**: TBD
- **Status**: proposed
- **Context**: How to aggregate token representations into a sentence embedding.
- **Alternatives**: Mean pooling, CLS token, last-token pooling
- **Decision**: TBD
