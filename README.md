# CRM Simples — FastAPI + PostgreSQL

Protótipo mínimo de um CRM (clientes, interações e oportunidades) usando **Python (FastAPI)** e **PostgreSQL**.

## Funcionalidades
- CRUD de **Clientes**
- CRUD de **Interações** ligadas a um cliente
- CRUD de **Oportunidades** com estágios simples (new, qualified, proposal, won, lost)
- Ordenação/filtragem básicas via query params
- CORS liberado (para facilitar testes com frontend)

## Como rodar (com Docker)
1. Copie o arquivo `.env.example` para `.env` e ajuste as variáveis, se quiser.
2. Suba o banco:
   ```bash
   docker compose up -d
   ```
3. Crie e ative um virtualenv (opcional) e instale dependências:
   ```bash
   python -m venv .venv && . .venv/bin/activate  # Linux/Mac
   # ou no Windows (PowerShell):
   # py -m venv .venv; .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
4. Execute as migrações iniciais (criação de tabelas):
   ```bash
   # As tabelas são criadas automaticamente no primeiro start do app (SQLAlchemy ORM).
   # Se preferir Alembic, dá para adicionar depois.
   ```
5. Rode a API:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Acesse a documentação interativa:
   - Swagger UI: http://127.0.0.1:8000/docs
   - Redoc: http://127.0.0.1:8000/redoc

## Endpoints principais
- `GET /health` — healthcheck
- **Clientes**
  - `POST /customers`
  - `GET /customers`
  - `GET /customers/{customer_id}`
  - `PUT /customers/{customer_id}`
  - `DELETE /customers/{customer_id}`
- **Interações**
  - `POST /customers/{customer_id}/interactions`
  - `GET /customers/{customer_id}/interactions`
  - `DELETE /interactions/{interaction_id}`
- **Oportunidades**
  - `POST /customers/{customer_id}/opportunities`
  - `GET /customers/{customer_id}/opportunities`
  - `PUT /opportunities/{opportunity_id}`
  - `DELETE /opportunities/{opportunity_id}`

## Notas
- Autenticação não inclusa (para manter simples). Pode-se adicionar JWT (Auth0, Firebase Auth ou lib simples) depois.
- Para rodar sem Docker, basta ter um PostgreSQL local e configurar `DATABASE_URL` no `.env`.