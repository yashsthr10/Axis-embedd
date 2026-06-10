# Inference server image.
# Build:  make docker-build
# Run:    make docker-up

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    TINYEMBED_HOST=0.0.0.0 \
    TINYEMBED_PORT=8000

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------
FROM base AS deps

COPY requirements.txt pyproject.toml README.md ./
COPY src/ src/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -e . --no-deps

# ---------------------------------------------------------------------------
# Runtime
# ---------------------------------------------------------------------------
FROM deps AS runtime

COPY configs/ configs/
COPY deployment/export/ deployment/export/
COPY scripts/ scripts/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${TINYEMBED_PORT}/health || exit 1

CMD ["python", "-m", "inference.server", "--config", "configs/inference.yaml"]
