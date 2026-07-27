# Track Money

Monorepo de portfolio para um sistema de gestao financeira com **backend FastAPI em DDD** e **frontend em HTML, CSS e JavaScript puro**.

## Estrutura

```text
track-money/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── .env.example
│   ├── Dockerfile
│   ├── endpoint.http
│   ├── init.sql
│   ├── pyproject.toml
│   └── README.md
├── frontend/
│   ├── assets/
│   ├── css/
│   ├── js/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── accounts.html
│   ├── profile.html
│   └── plans.html
├── docs/
│   └── architecture.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
└── LICENSE
```

## Organizacao

- `backend/` e autocontido: codigo FastAPI, testes, configuracao Python e artefatos de banco.
- `frontend/` concentra a interface estatica e pode ser publicada separadamente depois.
- `docs/` guarda a documentacao de arquitetura do monorepo.
- A raiz fica responsavel por orquestracao, CI e documentacao principal.

Essa estrutura mantem tudo no mesmo projeto hoje, mas facilita separar `backend/` e `frontend/` em repositorios distintos no futuro.

## Como executar

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

API: `http://localhost:8000`
Swagger: `http://localhost:8000/docs`

### Banco de dados

```bash
docker compose up -d
```

PostgreSQL: `localhost:5437`

### Frontend

Sirva a pasta `frontend/` com um servidor estatico. Exemplo:

```bash
cd frontend
python -m http.server 5500
```

Frontend: `http://localhost:5500`

## Qualidade

### Backend

```bash
cd backend
uv run ruff check .
uv run mypy .
uv run pytest -v
```

### Frontend

```bash
Get-ChildItem frontend\js -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
```

## Documentacao adicional

- Arquitetura: `docs/architecture.md`
- Guia do backend: `backend/README.md`
