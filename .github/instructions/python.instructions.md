---
applyTo: "**/*.py"
description: "Use when creating or modifying Python code in this FastAPI modular monolith."
---

# Python File Instructions

## Mandatory Architecture Alignment
- Keep code inside the correct bounded context (`authentication`, `subscription`, `movements`).
- Preserve modular monolith boundaries; avoid cross-context coupling.
- Keep business rules in domain/application layers, not in routers or ORM plumbing.

## DDD-Oriented Implementation Rules
- Model domain language explicitly in class/function names.
- Use entities/value objects for business concepts when appropriate.
- Place use-case orchestration in application services.
- Keep infrastructure concerns (database, external adapters) isolated in infra modules.

## FastAPI Rules
- Route handlers should orchestrate request/response only.
- Validate input with Pydantic schemas.
- Translate domain/application errors to HTTP responses at the boundary.
- Keep endpoint contracts stable and explicit.

## SQLAlchemy Rules
- Keep SQLAlchemy session usage controlled and explicit.
- Do not embed domain validations in persistence-only code.
- Use environment-driven database configuration (`DATABASE_URL`).

## Clean Code Rules
- Prefer small, composable functions.
- Remove dead code and unclear naming.
- Avoid broad exception handling; catch specific errors when needed.
- Avoid `any`-style typing shortcuts; keep type hints meaningful.

## Testing Expectations
- Add or update tests when behavior changes.
- Prioritize use-case tests and API contract tests for critical flows.
