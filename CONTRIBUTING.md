# Contributing to Track Money

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Docker and Docker Compose

```bash
uv sync
```

---

## Code quality tools

```bash
# Linter and formatter
uv run ruff check .
uv run ruff format .

# Type checker
uv run mypy .

# Tests
uv run pytest
```

All checks must pass before opening a pull request.

---

## Project architecture

This project follows **Domain-Driven Design (DDD)** in a **modular monolith** architecture.

### Bounded contexts

| Module | Responsibility |
|---|---|
| `autentication` | Registration, sign-in, JWT tokens |
| `subscription` | Plans, billing eligibility _(future)_ |
| `movements` | Accounts, categories, transactions _(future)_ |

**Rule:** modules must not import directly from each other. Cross-context communication happens through defined interfaces or shared kernel only.

### Layer responsibilities

```
router.py          → HTTP only: receive request, call use case, return response
use_cases/         → Business logic: pure functions, no FastAPI dependencies
domain (_user.py)  → Entities and value objects with invariants
infra              → Database, external adapters
```

#### Router (`router.py`)
- Declares endpoints with `APIRouter`
- Validates input with Pydantic schemas
- Calls use cases and translates exceptions to HTTP responses
- **Must not** contain business logic

```python
# ✅ correct
def create_user(body: UserCreate, ...):
    try:
        user = register_user(body, user_repository)
    except EmailAlreadyRegisteredError as e:
        return JSONResponse(status_code=400, ...)
    return JSONResponse(status_code=201, ...)

# ❌ wrong — business rule in the router
def create_user(body: UserCreate, ...):
    if user_repository.get_by_email(body.email):
        return JSONResponse(status_code=400, ...)
```

#### Use cases (`use_cases/`)
- Pure functions: receive domain types, return domain types or raise exceptions
- **No** FastAPI imports (`Depends`, `HTTPException`, etc.)
- Independently testable without starting the application

```python
# ✅ correct
def register_user(body: UserCreate, user_repository: UserRepository) -> _User:
    if user_repository.get_by_email(body.email):
        raise EmailAlreadyRegisteredError("Email already registered")
    ...

# ❌ wrong — FastAPI dependency inside use case
async def register_user(user_repository = Depends(get_user_repository)):
    ...
```

---

## Naming conventions

### Files

| Pattern | Meaning | Example |
|---|---|---|
| `_name.py` | Internal to the module — do not import outside the bounded context | `_user.py`, `_password.py` |
| `name.py` | Public interface of the module | `router.py`, `schema.py` |
| `use_cases/name.py` | One file per use case | `authenticate_user.py` |

### Python

| Element | Convention | Example |
|---|---|---|
| Classes | `PascalCase` | `UserRepository` |
| Functions and variables | `snake_case` | `get_user_profile` |
| Exceptions | `PascalCase` + `Error` suffix | `InvalidCredentialsError` |
| Constants | `UPPER_SNAKE_CASE` | `BCRYPT_MAX_BYTES` |
| Strings | Double quotes `"` | `"bearer"` |

### Exceptions

Domain exceptions are raised in use cases and translated to HTTP responses in the router:

```python
# use_cases/register_user.py
class EmailAlreadyRegisteredError(Exception):
    pass

# router.py
except EmailAlreadyRegisteredError as e:
    return JSONResponse(status_code=400, content={"message": str(e)})
```

---

## Adding a new endpoint

1. Create the use case in `use_cases/<action>_<entity>.py`
2. Add the schema (input/output) in `schema.py`
3. Register the route in `router.py`, calling the use case
4. Run `ruff check .` and `mypy .` before committing
