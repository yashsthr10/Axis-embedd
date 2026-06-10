# notebooks

Exploratory analysis and visualization. Not for production code.

## Intended use

- Inspect dataset quality (token distributions, pair statistics)
- Visualize training curves and eval scores
- Prototype new loss functions or data augmentations
- Compare experiment results side by side
- Debug model attention patterns

## Rules

- Notebooks are for exploration only. Production code extracted from notebooks goes into the appropriate module folder.
- Do not commit large notebook outputs (plots, dataframes) — clear outputs before committing or add to `.gitignore`.
- Reference experiment data by path (`experiments/<run_id>/`), never embed results inline.
- Name notebooks descriptively: `01_dataset_exploration.ipynb`, `02_loss_comparison.ipynb`.

## Suggested notebooks

| Notebook | Purpose |
|----------|---------|
| `01_dataset_exploration.ipynb` | Corpus stats, language distribution, dedupe impact |
| `02_tokenizer_analysis.ipynb` | Vocab coverage, token length distribution |
| `03_training_curves.ipynb` | Loss, LR, throughput over training |
| `04_eval_comparison.ipynb` | Compare MTEB scores across experiments |
| `05_inference_profiling.ipynb` | Latency breakdown, memory usage |
