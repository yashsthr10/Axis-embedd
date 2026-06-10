# data

Storage for raw and intermediate data artifacts. This folder holds data; processing logic lives in `src/dataset/`.

## Layout

```
data/
  raw/           Original downloads — never modify in place
  cleaned/       Output of dataset/clean/
  deduped/       Output of dataset/dedupe/
  processed/     Output of dataset/preprocess/
  pairs/         Output of dataset/pair_generation/
  final/         Train/val/test splits from dataset/builders/
```

## Rules

- Large files and datasets should be gitignored; only `.gitkeep` placeholders live in version control.
- Document data provenance (source, date, license) in `experiments/` or `docs/Dataset.md`.
- Never store checkpoints or model weights here — those belong in `experiments/`.

## Gitignore

Add to `.gitignore`:

```
data/raw/**
data/cleaned/**
data/deduped/**
data/processed/**
data/pairs/**
data/final/**
!data/**/.gitkeep
```
