# 💰 Track Money

REST API for personal finance management, built with **FastAPI** and **PostgreSQL**, following **Domain-Driven Design (DDD)** principles in a modular monolith architecture.

---

## 🚀 Technologies

| Layer | Technology |
|---|---|
| Web framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Database | [PostgreSQL 18](https://www.postgresql.org/) |
| ORM | [SQLAlchemy 2](https://www.sqlalchemy.org/) |
| Password hashing | [bcrypt](https://pypi.org/project/bcrypt/) |
| ASGI server | [Uvicorn](https://uvicorn.dev/) |
| Package manager | [uv](https://docs.astral.sh/uv/) |
| Linter / Formatter | [Ruff](https://docs.astral.sh/ruff/) |
| Type checker | [Mypy](https://mypy.readthedocs.io/) |
| Tests | [Pytest](https://docs.pytest.org/) |

---

## 📁 Project structure

```
track-money/
├── app/
│   ├── main.py                        # Application entry point
│   ├── authentication/                # Authentication bounded context (DDD)
│   │   ├── _user.py                   # User domain entity
│   │   ├── _password.py               # Password hash/verification utility
│   │   ├── _auth.py                   # JWT token generation
│   │   ├── _user_repository.py        # User persistence
│   │   ├── get_email_from_token.py    # JWT decode dependency
│   │   ├── query_user_by_email.py     # Cross-context user query (shared adapter)
│   │   ├── router.py                  # HTTP endpoints
│   │   ├── schema.py                  # Pydantic schemas (input/output)
│   │   └── use_cases/                 # Use cases: register, authenticate, profile
│   ├── subscription/                  # Subscription bounded context (DDD)
│   │   ├── plan/                      # Plan domain model and repository
│   │   ├── user/                      # Subscription user model and repository
│   │   ├── use_cases/                 # Use cases: select plan, get user
│   │   ├── router.py                  # HTTP endpoints
│   │   └── schema.py                  # Pydantic schemas
│   ├── movement/                      # Movement bounded context — core domain (DDD)
│   │   ├── bank/                      # BankAccount domain entity and repository
│   │   ├── use_cases/                 # Use cases: register bank account
│   │   ├── router.py                  # HTTP endpoints
│   │   └── schema.py                  # Pydantic schemas
│   ├── core/
│   │   └── domain_error.py            # Base domain exception
│   └── infra/
│       └── database.py                # SQLAlchemy configuration and session
├── tests/                             # Automated tests
├── docker-compose.yml                 # PostgreSQL via Docker
├── init.sql                           # Database initialization script
├── endpoint.http                      # HTTP request examples
└── pyproject.toml                     # Dependencies and configuration
```

---

## ⚙️ Prerequisites

- [Python 3.14+](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Docker](https://www.docker.com/) and Docker Compose

---

## 🏁 How to run

### 1. Clone the repository

```bash
git clone <repository-url>
cd track-money
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Start the database

```bash
docker compose up -d
```

PostgreSQL will be available at `localhost:5437`.

### 4. Start the API

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

Interactive documentation (Swagger): `http://localhost:8000/docs`

---

## 🔌 Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{ "status": "ok" }
```

---

### Create user

```http
POST /users/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@email.com",
  "password": "password123"
}
```

**Success response — `201 Created`:**
```json
{
  "message": "User created successfully",
  "user_id": 1
}
```

**Domain error response — `400 Bad Request`:**
```json
{
  "detail": "Email must be a non-empty string with a maximum length of 128 characters."
}
```

#### Domain validation rules

| Field | Rule |
|---|---|
| `name` | Required, max 128 characters |
| `email` | Required, must contain `@`, max 128 characters |
| `password` | Required, min 8 characters and max 72 bytes in UTF-8 (stored with bcrypt) |

---

### Create bank account

Requires authentication.

```http
POST /movement/bank-accounts
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "My Account",
  "bank_name": "Banco do Brasil",
  "account_number": "123456",
  "initial_balance": 1000.00
}
```

**Success response — `201 Created`:**
```json
{ "message": "Bank account created successfully" }
```

**Domain validation rules**

| Field | Rule |
|---|---|
| `name` | Required, max 24 characters |
| `bank_name` | Required, max 24 characters |
| `account_number` | Required, max 24 characters |
| `initial_balance` | Optional, non-negative decimal (default `0.0`) |

---

## 🗄️ Database

The application uses the `authentication` schema within the `track_money_db` database.

| Parameter | Default value |
|---|---|
| Host | `localhost` |
| Port | `5437` |
| Database | `track_money_db` |
| User | `postgres` |
| Password | `postgres` |

To use a custom URL, set the environment variable:

```bash
DATABASE_URL=postgresql://user:password@host:port/dbname
```

---

## 🧪 Tests

```bash
uv run pytest
```

## 🔍 Linter and type check

```bash
# Linter
uv run ruff check .

# Type checker
uv run mypy .
```
