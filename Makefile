.PHONY: help setup install install-dev install-cuda clean \
        train eval infer export benchmark test lint format typecheck check \
        docker-build docker-up docker-down docker-logs

# ---------------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------------
PYTHON       ?= python3
VENV         ?= .venv
BIN          ?= $(VENV)/bin
PIP          ?= $(BIN)/pip
PY           ?= $(BIN)/python

export PYTHONPATH := src

CONFIG_DIR   ?= configs
TRAIN_CONFIG ?= $(CONFIG_DIR)/train.yaml
EVAL_CONFIG  ?= $(CONFIG_DIR)/eval.yaml
INFER_CONFIG ?= $(CONFIG_DIR)/inference.yaml
TOKEN_CONFIG ?= $(CONFIG_DIR)/tokenizer.yaml

EXPERIMENT   ?= experiment_001
CHECKPOINT   ?= experiments/$(EXPERIMENT)/checkpoints/best
EXPORT_DIR   ?= deployment/export

DOCKER_IMAGE ?= tiny-embed
DOCKER_TAG   ?= latest
COMPOSE_FILE ?= deployment/docker-compose.yaml

# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------
help: ## Show available targets
	@grep -E '^[a-zA-Z0-9_.-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
setup: ## Create virtualenv and install all dependencies
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"
	$(PIP) install -r requirements-dev.txt
	$(PY) -m ipykernel install --user --name=tiny-embed --display-name="Python (tiny-embed)"
	@echo "Setup complete. Activate with: source $(VENV)/bin/activate"
	@echo "Notebook kernel: Python (tiny-embed)"

install: ## Install production dependencies only
	$(PIP) install -e .

install-dev: ## Install with dev, lint, and test tools
	$(PIP) install -e ".[dev]"

install-cuda: ## Install with CUDA kernel build dependencies
	$(PIP) install -e ".[cuda]"

clean: ## Remove build artifacts, caches, and virtualenv
	rm -rf $(VENV) build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find src -name "*.so" -delete 2>/dev/null || true

# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
train: ## Run training loop
	$(PY) -m training.trainer --config $(TRAIN_CONFIG) --experiment $(EXPERIMENT)

eval: ## Run evaluation benchmarks
	$(PY) -m evaluation.mteb_runner --config $(EVAL_CONFIG) --checkpoint $(CHECKPOINT)

infer: ## Start inference server
	$(PY) -m inference.server --config $(INFER_CONFIG)

export: ## Export checkpoint for deployment
	$(PY) scripts/export_model.py --checkpoint $(CHECKPOINT) --output $(EXPORT_DIR)

benchmark: ## Run inference benchmarks
	$(PY) benchmarks/latency/run.py --config $(INFER_CONFIG)

tokenize: ## Train tokenizer
	$(PY) -m tokenizer.train --config $(TOKEN_CONFIG)

fetch: ## Fetch raw data from Common Crawl
	$(PY) scripts/fetch_data.py

preprocess: ## Inspect, clean, dedupe, and analyze raw data
	$(PY) scripts/preprocess_data.py

# ---------------------------------------------------------------------------
# Quality
# ---------------------------------------------------------------------------
test: ## Run test suite
	$(BIN)/pytest tests/ -v

test-cuda: ## Run CUDA correctness tests (requires GPU)
	$(BIN)/pytest tests/cuda/ -v -m cuda

lint: ## Lint with ruff
	$(BIN)/ruff check src tests scripts benchmarks

format: ## Format code with ruff
	$(BIN)/ruff format src tests scripts benchmarks
	$(BIN)/ruff check --fix src tests scripts benchmarks

typecheck: ## Static type check with mypy
	$(BIN)/mypy src

check: lint typecheck test ## Run lint, typecheck, and tests

# ---------------------------------------------------------------------------
# Docker
# ---------------------------------------------------------------------------
docker-build: ## Build inference Docker image
	docker build -f deployment/Dockerfile -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

docker-up: ## Start inference server via docker compose
	docker compose -f $(COMPOSE_FILE) up -d --build

docker-down: ## Stop docker compose stack
	docker compose -f $(COMPOSE_FILE) down

docker-logs: ## Tail inference server logs
	docker compose -f $(COMPOSE_FILE) logs -f inference
