# experiments

Per-run artifacts: configs, results, graphs, and notes. Never lose an experiment.

## Layout

```
experiments/
  experiment_001/
    configs/          Snapshot of configs used for this run
    checkpoints/      Model checkpoints
    logs/             Training logs and metrics
    eval/             Evaluation results
    benchmarks/       Performance measurements
    notes.md          Human-readable observations
    plots/            Loss curves, eval charts
  experiment_002/
    ...
```

## What to store per experiment

| Artifact | Required |
|----------|----------|
| Config snapshot | Yes — copy of all `configs/*.yaml` at run start |
| Training logs | Yes |
| Best checkpoint | Yes |
| Eval results | Yes — after training completes |
| notes.md | Yes — what worked, what didn't, surprises |
| Plots | Recommended |
| Benchmarks | Recommended — before claiming production-ready |

## Naming convention

```
experiment_<NNN>_<short_description>/

Examples:
  experiment_001_baseline_mha/
  experiment_002_mla_flash/
  experiment_003_int8_inference/
```

## notes.md template

```markdown
# Experiment NNN: short description

- **Date**: YYYY-MM-DD
- **Config**: experiment_NNN/configs/
- **Goal**: What were we trying to achieve?
- **Result**: What happened?
- **Surprises**: Anything unexpected?
- **Next steps**: What to try next?
```

## Rules

- Never delete experiment directories — archive if needed.
- Config snapshot must be a copy, not a symlink, so it reflects the exact state at run time.
- Link relevant decisions to `docs/Decisions.md` entries.
