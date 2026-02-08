# Production-Ready Container Images

This directory contains production-optimized container images for the Todo + Chatbot application.

## Frontend Service (Node.js)

- **Base Image**: `node:18-alpine` for minimal attack surface
- **Multi-stage build**: Dependencies installed in builder stage, copied to production stage
- **Security**: Runs as non-root user (UID 1001)
- **Optimizations**:
  - Uses dumb-init for proper signal handling
  - Clean package cache after installation
  - Health checks with curl
- **Layers**: Optimized for Docker build cache efficiency

## Backend Service (Python/FastAPI)

- **Base Image**: `python:3.11-alpine` for minimal size
- **Multi-stage build**: Dependencies installed separately from application code
- **Security**: Runs as non-root user (UID 1000)
- **Optimizations**:
  - Uses dumb-init for proper signal handling
  - Pin dependencies with integrity checks
  - Health checks with curl
  - PostgreSQL client for database operations
- **Python-specific**:
  - Environment variables to prevent bytecode generation
  - Pip cache cleared after installation

## Chatbot Backend Service (Python)

- **Base Image**: `python:3.11-alpine` for minimal size
- **Multi-stage build**: Dependencies installed separately from application code
- **Security**: Runs as non-root user (UID 1000)
- **Optimizations**:
  - Uses dumb-init for proper signal handling
  - Pin dependencies with integrity checks
  - Health checks with curl
  - GCC and musl-dev for native compilation if needed
- **Python-specific**:
  - Environment variables to prevent bytecode generation
  - Pip cache cleared after installation

## Security Best Practices

- All containers run as non-root users
- ReadOnlyRootFilesystem disabled only where necessary
- Privilege escalation disabled
- Minimal packages installed (Alpine base images)
- Capabilities restricted (drop: ALL pattern applied in Kubernetes)

## Build Optimizations

- Multi-stage builds to minimize final image size
- Layer caching optimized through proper COPY ordering
- Package managers configured to clean caches
- Production-only dependencies installed

## Health Monitoring

- HEALTHCHECK instructions in all Dockerfiles
- Proper startup, liveness, and readiness probes configured in Kubernetes manifests
- HTTP-based health checks using curl
- Appropriate timeouts and retry configurations

## Operational Excellence

- Deterministic builds with pinned base image versions
- Structured logging ready
- Environment variable configuration
- Proper signal handling with dumb-init