# tokenizer

Vocabulary training and export. Transforms raw text into subword tokens.

**Owner**: Friend

## Layout

```
src/tokenizer/
  train.py            Train SentencePiece / BPE model on corpus
  export.py           Export to HuggingFace-compatible format
  sentencepiece/      SentencePiece training configs and scripts
  vocab/              Vocabulary inspection and analysis tools
```

## Outputs

| Artifact | Description |
|----------|-------------|
| `tokenizer.model` | SentencePiece binary model |
| `tokenizer.json` | HuggingFace-compatible tokenizer config |

## Pipeline

```
Corpus (from data/final/ or data/processed/)
     |
     v
train.py  <-- configs/tokenizer.yaml
     |
     v
tokenizer.model
     |
     v
export.py
     |
     v
tokenizer.json
```

## Configuration

All tokenizer hyperparameters live in `configs/tokenizer.yaml`:

- `vocab_size`
- `algorithm` (unigram, bpe, wordpiece)
- `special_tokens`
- `corpus_path`

## Usage

```bash
export PYTHONPATH=src
python -m tokenizer.train --config configs/tokenizer.yaml
python -m tokenizer.export --config configs/tokenizer.yaml
```

## Rules

- Tokenizer training is independent of model training.
- Export format must be compatible with the training dataloader and inference loader.
- Vocab changes require a new experiment ID and entry in `docs/Decisions.md`.
