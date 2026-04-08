---
globs: "**/Dockerfile*, **/docker-compose*, **/.dockerignore"
---
# Docker / Docker Compose Rules

## Dockerfile
- Use multi-stage builds (builder → runner).
- Final image: minimal base (alpine or distroless).
- Chain RUN commands with && to minimize layers.
- No hardcoded secrets (API keys, passwords) in ARG/ENV.

## Docker Compose
- healthcheck required for every service.
- Persist data with volume mounts (PostgreSQL, MinIO).
- Reference env vars from .env file. No inline values.
- Define networks explicitly.

## General
- .dockerignore must include: node_modules, __pycache__, .env
- Split compose files by environment:
  docker-compose.yml (base) + docker-compose.dev.yml + docker-compose.prod.yml
