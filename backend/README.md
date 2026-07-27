# Track Money Backend

Backend em **FastAPI + PostgreSQL** para o Track Money, organizado em **DDD** dentro de um monorepo.

## Estrutura interna

```text
backend/
├── app/
│   ├── main.py
│   ├── authentication/
│   ├── subscription/
│   ├── movement/
│   ├── core/
│   └── infra/
├── tests/
├── .env.example
├── Dockerfile
├── endpoint.http
├── init.sql
├── pyproject.toml
└── uv.lock
```

## Contextos

- `authentication`: cadastro, login, JWT e perfil
- `subscription`: planos e assinatura do usuario
- `movement`: contas bancarias e evolucao futura de movimentacoes

## Executando localmente

```bash
uv sync
docker compose up -d
uv run uvicorn app.main:app --reload
```

> Rode os comandos a partir da pasta `backend/`, exceto `docker compose`, que continua na raiz do repositorio.

## Variaveis de ambiente

Copie `backend/.env.example` para `backend/.env` e ajuste conforme necessario.

Principais variaveis:
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `ALGORITHM`
- `FRONTEND_ORIGINS`

## Comandos de qualidade

```bash
uv run ruff check .
uv run mypy .
uv run pytest -v
```

## Endpoints ja disponiveis

- `POST /users`
- `POST /users/token`
- `GET /users/profile`
- `GET /subscription/plans`
- `POST /subscription/select-plan`
- `GET /subscription/user`
- `GET /movement/bank-accounts`
- `POST /movement/bank-accounts`
