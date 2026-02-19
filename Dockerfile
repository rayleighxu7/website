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

# Inject Open Graph meta tags into Streamlit's index.html for link previews
RUN STHTML=$(python -c "import streamlit, pathlib; print(pathlib.Path(streamlit.__file__).parent / 'static' / 'index.html')") && \
    sed -i 's|</head>|<meta property="og:title" content="freelanxur" />\n<meta property="og:description" content="Data Engineer \&amp; Consultant" />\n<meta property="og:type" content="website" />\n<meta property="og:url" content="https://freelanxur.com" />\n<meta name="twitter:card" content="summary" />\n<meta name="twitter:title" content="freelanxur" />\n<meta name="twitter:description" content="Data Engineer \&amp; Consultant" />\n</head>|' "$STHTML"

# Streamlit config
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

ENTRYPOINT ["/app/.venv/bin/streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--browser.gatherUsageStats=false"]

