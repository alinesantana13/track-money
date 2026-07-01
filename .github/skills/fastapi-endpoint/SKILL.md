---
name: fastapi-endpoint
description: "Use when creating or refactoring FastAPI endpoints in this DDD modular monolith."
---

# Skill: FastAPI Endpoint (DDD + Modular Monolith)

## Purpose
Create endpoints that are production-ready, maintainable, and aligned with domain boundaries.

## When to Use
- Adding a new endpoint.
- Refactoring an existing endpoint.
- Standardizing endpoint structure for portfolio-level quality.

## Workflow
1. Identify bounded context (`autentication`, `subscription`, or `movement`).
2. Define request/response schemas with clear contracts.
3. Keep router/controller thin and delegate business logic to application service/use case.
4. Ensure domain validations stay in domain/application layer.
5. Integrate persistence through repository/infra abstractions.
6. Map domain/application errors to HTTP responses.
7. Add/update tests for endpoint contract and use-case behavior.
8. Run lint and tests.

## Quality Checklist
- Endpoint is inside the correct module/context.
- No business rule is hardcoded in the router.
- Input validation and output contract are explicit.
- HTTP status codes are correct and consistent.
- Code is readable and easy to review on GitHub.

## Example Prompts
- "Create a POST endpoint to add a transaction in the movements context."
- "Refactor user registration endpoint to keep business logic out of the router."
