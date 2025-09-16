# CRM  — FastAPI + PostgreSQL

Protótipo de um CRM (clientes, interações e oportunidades) usando **Python (FastAPI)** e **PostgreSQL**.

## Funcionalidades
- CRUD de **Clientes**
- CRUD de **Interações** ligadas a um cliente
- CRUD de **Oportunidades** com estágios simples (new, qualified, proposal, won, lost)
- Ordenação/filtragem básicas via query params
- CORS liberado (para facilitar testes com frontend)



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
