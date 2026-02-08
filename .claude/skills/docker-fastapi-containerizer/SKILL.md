---
name: docker-fastapi-containerizer
description: |
  This skill helps containerize Python/FastAPI applications from hello world to professional production deployments. It provides best practices for Dockerfiles, multi-stage builds, security configurations, and Docker Compose setups for Python/FastAPI applications. Use when users need to create Docker artifacts for their Python/FastAPI projects. Now uses uv as the default dependency manager for 10-100x faster performance.
allowed-tools: Read, Grep, Glob, Bash
---

# Docker FastAPI Containerizer with uv

This skill helps containerize Python/FastAPI applications from hello world to professional production deployments, following Docker best practices and security guidelines. Now uses uv as the default dependency manager for 10-100x faster performance.

## What This Skill Does

- Creates optimized Dockerfiles for Python/FastAPI applications with uv dependency management
- Implements multi-stage builds for reduced image size and enhanced security
- Sets up Docker Compose configurations for multi-service applications
- Applies security best practices (non-root users, hardened images)
- Provides production-ready configurations with uv for fast dependency installation

## When to Use This Skill

Use when users need to containerize Python/FastAPI applications with proper security, performance, and maintainability considerations using uv for dependency management.

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing Python/FastAPI application structure, pyproject.toml/requirements.txt, entry points |
| **Conversation** | User's specific deployment requirements, environment constraints |
| **Skill References** | Docker best practices from `references/` (multi-stage builds, security, production configs) |
| **User Guidelines** | Team-specific conventions, security policies |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## uv Dependency Management Best Practices

### 1. uv Installation in Docker

Use the official uv binary from the container registry:

```dockerfile
# Install uv
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies with uv
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-workspace
```

### 2. Multi-Stage Builds with uv

Use multi-stage builds to separate build-time dependencies from runtime image:

```dockerfile
#syntax=docker/dockerfile:1

# === Build stage: Install dependencies and create virtual environment with uv ===
FROM python:3.12-slim as builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install dependencies with uv
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv --seed && \
    uv sync --locked --no-dev --inexact

# === Final stage: Create minimal runtime image ===
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

COPY app.py ./
COPY --from=builder /app/.venv /app/.venv

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/.venv/bin/python", "app.py"]
```

### 3. uv Production Optimizations

- Enable bytecode compilation for faster startup: `ENV UV_COMPILE_BYTECODE=1`
- Use cache mounts to speed up builds: `--mount=type=cache,target=/root/.cache/uv`
- Use frozen lock files: `uv sync --frozen`
- Enable copy mode for cache compatibility: `ENV UV_LINK_MODE=copy`

## Dockerfile Best Practices for Python/FastAPI Applications

### 1. Multi-Stage Builds with uv

Use multi-stage builds to separate build-time dependencies from runtime image:

```dockerfile
#syntax=docker/dockerfile:1

# === Build stage: Install dependencies with uv ===
FROM python:3.12-slim as builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install dependencies with uv (faster than pip)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv --seed && \
    uv sync --locked --no-dev --inexact

# === Final stage: Create minimal runtime image ===
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

COPY app.py ./
COPY --from=builder /app/.venv /app/.venv

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/.venv/bin/python", "app.py"]
```

### 2. Security Best Practices

- Use non-root users to reduce attack surface
- Implement Docker Hardened Images (DHI) when available
- Set environment variables to prevent bytecode generation and buffering
- Minimize installed packages in final image

### 3. Production Optimizations with uv

- Use uv for 10-100x faster dependency installation
- Enable bytecode compilation: `ENV UV_COMPILE_BYTECODE=1`
- Use cache mounts: `--mount=type=cache,target=/root/.cache/uv`
- Use frozen lock files: `uv sync --frozen`
- Clean up build dependencies in final stage

## Docker Compose Configuration

For multi-service applications, use Docker Compose with production-ready configurations:

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      target: production
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

## Production Deployment Patterns

### 1. Hello World to Production Scale

For simple applications:
- Basic Dockerfile with single stage
- Direct uvicorn command execution
- uv for fast dependency installation

For production applications:
- Multi-stage builds with uv
- Health checks
- Proper logging
- Resource limits
- Security configurations

### 2. Environment-Specific Configurations

Different configurations for development, staging, and production:

Development:
- Volume mounts for hot reloading
- Debug mode enabled
- Additional development tools
- uv for fast dependency installation

Production:
- Optimized base images
- Security hardening
- Resource constraints
- Health checks
- uv with bytecode compilation

## Implementation Workflow

### Step 1: Analyze Application Structure
- Identify pyproject.toml or requirements.txt
- Locate application entry point
- Determine exposed port
- Identify additional dependencies

### Step 2: Choose Dockerfile Pattern
- Simple: Single-stage for basic applications
- Multi-stage: For production with optimized size and uv
- Custom: With specific base image requirements

### Step 3: Apply Security Measures
- Create non-root user
- Use minimal base images
- Remove unnecessary packages
- Set appropriate environment variables

### Step 4: Optimize for Production with uv
- Implement multi-stage builds with uv
- Configure proper logging
- Add health checks
- Set resource limits
- Enable bytecode compilation with `ENV UV_COMPILE_BYTECODE=1`

### Step 5: Create Supporting Files
- Docker Compose for multi-service apps
- .dockerignore file
- Build scripts if needed

## Common Dockerfile Patterns

### Basic FastAPI Application with uv
```dockerfile
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
# Enable bytecode compilation for faster startup
ENV UV_COMPILE_BYTECODE=1

# Install dependencies with uv (much faster than pip)
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv --seed && \
    uv sync --locked --no-dev

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Multi-Stage with uv Builder Pattern
```dockerfile
#syntax=docker/dockerfile:1

FROM python:3.12-slim as builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

WORKDIR /app

# Install build dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies with uv in builder stage
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv --seed && \
    uv sync --locked --no-dev --inexact

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

# Copy installed packages from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Docker Ignore Patterns

Create a `.dockerignore` file to exclude unnecessary files:

```
**/.git
**/.gitignore
**/.dockerignore
**/.env
**/.venv
**/venv
**/requirements-dev.txt
**/Dockerfile*
**/docker-compose*
**/.DS_Store
**/README.md
**/LICENSE
**/*.log
**/__pycache__
**/*.pyc
**/*.pyo
**/*.pyd
**/.pytest_cache
**/.coverage
**/htmlcov
**/node_modules
**/uv.lock
```

## Health Checks for Production

Add health checks to monitor application status:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

## Quality Checklist

Before finalizing Docker setup, ensure:

- [ ] Multi-stage build implemented with uv for production
- [ ] Non-root user configured
- [ ] Minimal base image used
- [ ] Environment variables properly set (including UV_COMPILE_BYTECODE=1)
- [ ] Proper logging configuration
- [ ] .dockerignore file created
- [ ] Docker Compose available for multi-service
- [ ] Health checks implemented
- [ ] Security scan passed
- [ ] Resource limits configured
- [ ] uv used instead of pip for dependency management