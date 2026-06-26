---
name: docker-setup
description: "Use when configuring or reviewing Docker setup for local development of this FastAPI + PostgreSQL project."
---

# Skill: Docker Setup (FastAPI + PostgreSQL)

## Purpose
Provide a reliable Docker setup for local development with clear, reproducible configuration.

## When to Use
- Creating initial Docker files.
- Updating Docker Compose services.
- Debugging local environment/database startup issues.

## Workflow
1. Define required services (at minimum: PostgreSQL; optionally API service).
2. Configure environment variables explicitly (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`).
3. Expose container ports clearly and keep app config aligned (for this project, host `5437` maps to container `5432`).
4. Add healthchecks for database readiness.
5. Configure persistent volumes for database data.
6. Keep initialization scripts explicit (`init.sql`) when needed.
7. Ensure app database URL uses environment variable with sensible fallback.
8. Validate by starting containers and testing connectivity.

## Quality Checklist
- `docker-compose.yml` is readable and deterministic.
- Port mapping is documented and consistent with `DATABASE_URL`.
- Database service has a healthcheck and persistent volume.
- No secrets are hardcoded beyond local-dev defaults.
- Developer can start environment with one command and connect successfully.

## Example Prompts
- "Set up docker-compose for FastAPI and PostgreSQL with healthcheck."
- "Fix database connection mismatch between app config and compose ports."
