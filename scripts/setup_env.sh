#!/usr/bin/env bash
# Bootstrap local development environment.
# Usage: ./scripts/setup_env.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Creating virtual environment"
python3 -m venv .venv
source .venv/bin/activate

echo "==> Installing dependencies"
pip install --upgrade pip
pip install -e ".[dev]"

echo "==> Setting up pre-commit hooks"
pre-commit install || echo "pre-commit not available, skipping"

if [ ! -f .env ]; then
    echo "==> Creating .env from .env.example"
    cp .env.example .env
fi

echo "==> Verifying Python path"
export PYTHONPATH=src
python -c "import model, training, evaluation, inference; print('src/ modules importable')" \
    || echo "Modules not yet implemented — structure is ready"

if command -v nvidia-smi &>/dev/null; then
    echo "==> GPU detected"
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
else
    echo "==> No GPU detected — training and CUDA tests will run on CPU"
fi

echo ""
echo "Setup complete."
echo "  source .venv/bin/activate"
echo "  make help"
