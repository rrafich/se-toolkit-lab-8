# Multi-stage Dockerfile for nanobot gateway
# Pattern: backend/Dockerfile

# ---
# Stage 1: Build the application in the `/app` directory
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy root workspace files for additional_contexts
COPY --from=workspace pyproject.toml uv.lock /app/

# Copy nanobot source
COPY . /app/nanobot

# Copy entire nanobot-websocket-channel for workspace sources
COPY --from=workspace nanobot-websocket-channel /app/nanobot-websocket-channel

# Copy mcp directory for workspace sources  
COPY --from=workspace mcp /app/mcp

# Install nanobot with dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# ---
# Stage 2: Final image without uv
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

ARG APP_UID=1000
ARG APP_GID=1000

RUN groupadd --system --gid ${APP_GID} appgroup \
    && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home appuser

COPY --from=builder --chown=appuser:appgroup /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER appuser
WORKDIR /app

CMD ["python", "/app/nanobot/entrypoint.py"]
