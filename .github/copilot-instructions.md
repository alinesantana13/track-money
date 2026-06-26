# Copilot Instructions for Track Money

## Project Context
- This project is a **personal finance system**.
- Architecture: **Modular Monolith**.
- Design approach: **Domain-Driven Design (DDD)**.
- Organize code by **bounded context**, not by technical layer only.

## Bounded Contexts
1. **Authentication**
   - Responsibilities: user registration, sign-in, credential management.
   - Domain model: `User` with sensitive data (email, password hash, auth rules).

2. **Subscription**
   - Responsibilities: subscription plans, billing eligibility, account limits by plan.
   - Domain model: `User` representation focused on billing/subscription data (no password).

3. **Movements (Core Domain)**
   - Responsibilities: financial operations and money flow.
   - Main domain models: `Account`, `Category`, `Transaction`.
   - `User` here should be lightweight (for example, identity/email reference only).

## Architectural Rules
- Keep module boundaries explicit and enforceable.
- Prefer this dependency direction:
  - `interface/router -> application/use_cases -> domain`
  - `infra` implements ports/contracts owned by `application` or `domain`.
- Do not leak persistence or framework details into domain entities.
- Keep business rules in domain/application, not in routers.

## Code Quality Expectations
- Use clear, intention-revealing names.
- Small functions with a single responsibility.
- Avoid duplicated business rules across contexts.
- Handle errors explicitly; do not swallow exceptions silently.
- Use environment variables for infrastructure configuration.

## FastAPI and SQLAlchemy Conventions
- Use startup/lifespan hooks for app initialization.
- Keep route handlers thin; delegate business logic to services/use cases.
- Validate inputs with Pydantic schemas.
- Return consistent HTTP status codes and response contracts.

## Portfolio Readiness
- Favor readable architecture over clever shortcuts.
- Keep module boundaries and naming consistent for GitHub reviewers.
- Every change should improve maintainability and testability.
