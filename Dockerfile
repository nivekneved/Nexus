# ==============================================================================
# NEXUS AUTONOMOUS AI WORKFORCE - PRODUCTION DOCKERFILE
# Multi-stage lightweight Python 3.11 container with zero-regression sandboxing
# ==============================================================================

FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies needed for git recon and secure SSL handshakes
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specifications
COPY requirements.txt .

# Build wheels for fast deployment
RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final runtime image
FROM python:3.11-slim

WORKDIR /app

# Install runtime tools (git for Chief of Staff / Repo Radar, curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install pre-built python wheels
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Set enterprise environment flags
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=utf-8 \
    PORT=8000 \
    HOST=0.0.0.0

# Copy application code
COPY . .

# Ensure data directories exist and have proper permissions
RUN mkdir -p backups static scratch

# Expose Web Command Center Port
EXPOSE 8000

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/security/shield || exit 1

# Launch Nexus Autonomous Server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
