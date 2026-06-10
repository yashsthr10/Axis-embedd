# scripts

One-off and operational scripts that do not belong in a core module.

## Examples

| Script | Purpose |
|--------|---------|
| `download_corpus.sh` | Fetch raw training data |
| `export_model.py` | Convert checkpoint to inference format |
| `compare_checkpoints.py` | Diff two model checkpoints |
| `profile_inference.py` | Quick latency profiling |
| `setup_env.sh` | Install dependencies and verify GPU |

## Rules

- Scripts are thin wrappers around module code — business logic stays in `src/model/`, `src/training/`, etc.
- Scripts accept `--config` pointing to `configs/`; no hardcoded paths.
- Document each script with a one-line comment at the top of the file.
- Destructive operations (delete data, overwrite checkpoints) require explicit `--force` flag.

## Usage

```bash
./scripts/setup_env.sh
python scripts/export_model.py --checkpoint experiments/run_001/checkpoints/best/ --output deployment/
```
