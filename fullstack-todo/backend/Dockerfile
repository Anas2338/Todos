#syntax=docker/dockerfile:1

# === Build stage: Install dependencies with uv ===
FROM python:3.13-alpine AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Set environment variable to handle pydantic-core build issue with newer Python versions
ENV PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1

# Install dependencies with uv (faster than pip)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv venv --seed --python python3.13 && \
    uv sync --locked --no-dev --no-install-project

FROM python:3.13-alpine AS production

# Install only runtime dependencies
RUN apk add --no-cache --no-progress dumb-init postgresql-client && \
    addgroup -g 1000 -S appgroup && \
    adduser -u 1000 -S appuser -G appgroup

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appgroup . .

# Create directory for SQLite database if needed and set permissions
RUN mkdir -p /app/data && chown appuser:appgroup /app/data

# Switch to non-root user
USER appuser

EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import requests; r = requests.get('http://localhost:7860/health'); exit(0 if r.status_code == 200 else 1)" || exit 1

# Use dumb-init to handle signals properly
ENTRYPOINT ["/usr/bin/dumb-init"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]