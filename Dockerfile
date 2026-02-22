# ── Build stage: install dependencies with uv ─────────────────────────────────
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install dependencies first (layer cache)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy project source
COPY . .

# ── Runtime stage ──────────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy the entire virtualenv + source from builder
COPY --from=builder /app /app

# Streamlit config
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

# used for AWS ECS Fargate
# ENTRYPOINT ["/app/.venv/bin/streamlit", "run", "app.py", \
#     "--server.port=8501", \
#     "--server.address=0.0.0.0", \
#     "--server.headless=true", \
#     "--browser.gatherUsageStats=false"]

# used for Railway
ENTRYPOINT ["/bin/sh", "-c", "exec /app/.venv/bin/streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false"]

