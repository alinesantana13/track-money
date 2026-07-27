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
│   ├── Dockerfile
│   ├── config.template.js
│   ├── nginx.conf
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

1. Crie o arquivo de ambiente local:

```bash
cp .env.example .env
```

2. Inicie a aplicacao completa:

```bash
docker compose up --build
```

| Servico | URL local |
| --- | --- |
| Frontend | `http://localhost:8080` |
| API | `http://localhost:8000` |
| Swagger | `http://localhost:8000/docs` |
| PostgreSQL | `localhost:5437` |

## Deploy no EasyPanel

Publique o Compose como uma aplicacao e associe um dominio a cada servico HTTP:

| Servico | Porta interna | Dominio sugerido |
| --- | --- | --- |
| `frontend` | `80` | `app.seu-dominio.com` |
| `backend` | `8000` | `api.seu-dominio.com` |
| `postgres` | `5432` | Sem dominio publico |

Cadastre as variaveis abaixo no EasyPanel. Nao envie o arquivo `.env` para o repositorio.

```dotenv
POSTGRES_USER=track_money
POSTGRES_PASSWORD=<senha-forte>
POSTGRES_DB=track_money
DATABASE_URL=postgresql+psycopg2://track_money:<senha-codificada-para-url>@postgres:5432/track_money
JWT_SECRET_KEY=<segredo-longo-e-aleatorio>
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
FRONTEND_ORIGINS=https://app.seu-dominio.com
API_BASE_URL=https://api.seu-dominio.com
```

`API_BASE_URL` e gerada em `/config.js` quando o container do frontend inicia. Assim, a mesma imagem do frontend serve desenvolvimento e producao; basta alterar a variavel no EasyPanel e reiniciar somente o frontend. `FRONTEND_ORIGINS` aceita multiplos dominios separados por virgula.

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
