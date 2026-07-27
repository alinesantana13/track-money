# Arquitetura do Monorepo

## Visao geral

O Track Money foi reorganizado para um **monorepo com fronteiras explicitas**:

- `backend/` para a API e regras de negocio
- `frontend/` para a interface web
- `docs/` para documentacao arquitetural

Isso permite evoluir o sistema de forma integrada hoje e separar os modulos depois com baixo atrito.

## Backend

O backend segue um **modular monolith com DDD**:

- `authentication`
- `subscription`
- `movement`

Camadas compartilhadas:

- `app/core`
- `app/infra`

### Direcao de dependencias

```text
router -> use_cases -> domain
infra  -> implementacoes tecnicas
```

## Frontend

O frontend usa:

- HTML5
- CSS3
- JavaScript ES6

Organizacao principal:

```text
frontend/
├── css/
├── js/api/
├── js/components/
├── js/pages/
└── js/utils/
```

## Integracao

- autenticacao via JWT
- consumo da API com `fetch()`
- `Authorization: Bearer <token>`
- tratamento central de `401`

## Separacao futura

Se for necessario dividir o projeto:

1. `backend/` ja possui configuracao Python propria
2. `frontend/` ja possui estrutura propria
3. a raiz concentra apenas coordenacao e documentacao
