from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.security import OAuth2PasswordRequestForm
from . import auth

from .database import Base, engine, get_db
from . import crud, schemas, models

app = FastAPI(title="CRM Simples", version="0.1.0")

# Cria as tabelas automaticamente (para protótipo)
Base.metadata.create_all(bind=engine)

# CORS (liberar tudo para testes)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# ---- Customers ----
@app.post("/customers", response_model=schemas.CustomerOut, status_code=201)
def create_customer(payload: schemas.CustomerCreate, db: Session = Depends(get_db)):
    if payload.email:
        # garantir unicidade de email
        existing = crud.list_customers(db, q=payload.email, limit=1, offset=0)
        if any(c.email == payload.email for c in existing):
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
    return crud.create_customer(db, payload)

@app.get("/customers", response_model=List[schemas.CustomerOut])
def list_customers(
    q: Optional[str] = Query(default=None, description="Busca por nome/email/empresa"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    return crud.list_customers(db, q=q, limit=limit, offset=offset)

@app.get("/customers/{customer_id}", response_model=schemas.CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer

@app.put("/customers/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(customer_id: int, payload: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    updated = crud.update_customer(db, customer_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return updated

@app.delete("/customers/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_customer(db, customer_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return

# ---- Interactions ----
@app.post("/customers/{customer_id}/interactions", response_model=schemas.InteractionOut, status_code=201)
def create_interaction(customer_id: int, payload: schemas.InteractionCreate, db: Session = Depends(get_db)):
    # valida cliente
    if not crud.get_customer(db, customer_id):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud.create_interaction(db, customer_id, payload)

@app.get("/customers/{customer_id}/interactions", response_model=List[schemas.InteractionOut])
def list_interactions(customer_id: int, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    if not crud.get_customer(db, customer_id):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud.list_interactions(db, customer_id, limit=limit, offset=offset)

@app.delete("/interactions/{interaction_id}", status_code=204)
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_interaction(db, interaction_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Interação não encontrada")
    return

# ---- Opportunities ----
@app.post("/customers/{customer_id}/opportunities", response_model=schemas.OpportunityOut, status_code=201)
def create_opportunity(customer_id: int, payload: schemas.OpportunityCreate, db: Session = Depends(get_db)):
    if not crud.get_customer(db, customer_id):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud.create_opportunity(db, customer_id, payload)

@app.get("/customers/{customer_id}/opportunities", response_model=List[schemas.OpportunityOut])
def list_opportunities(customer_id: int, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    if not crud.get_customer(db, customer_id):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud.list_opportunities(db, customer_id, limit=limit, offset=offset)

@app.put("/opportunities/{opportunity_id}", response_model=schemas.OpportunityOut)
def update_opportunity(opportunity_id: int, payload: schemas.OpportunityUpdate, db: Session = Depends(get_db)):
    updated = crud.update_opportunity(db, opportunity_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada")
    return updated

@app.delete("/opportunities/{opportunity_id}", status_code=204)
def delete_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_opportunity(db, opportunity_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada")
    return




@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me")
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return {"email": current_user.email}


#cria usuarios
@app.post("/users", response_model=schemas.UserOut)
def create_user_endpoint(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, payload)



#Cria os endpois para as listas de usuarios e oportunidades

# ---- Opportunities (listagem geral) ----
@app.get("/opportunities", response_model=List[schemas.OpportunityOut])
def list_all_opportunities(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    return crud.list_all_opportunities(db, limit=limit, offset=offset)


# ---- Lisstagem de Users ----
@app.get("/users", response_model=List[schemas.UserOut])
def list_users(
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    return crud.list_users(db, limit=limit, offset=offset)

# ---- Buscar um Usuário pelo ID ----
@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user



@app.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    user: schemas.UserCreate,  # ideal seria um UserUpdate separado
    db: Session = Depends(get_db)
):
    updated = crud.update_user(db, user_id=user_id, user=user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

# A mesma lógica para Customer
# ---- Editar um Cliente ----
@app.put("/customers/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(
    customer_id: int,
    customer: schemas.CustomerCreate, # Use o esquema que representa os dados de criação/atualização
    db: Session = Depends(get_db)
):
    # Encontra o cliente no banco de dados pelo ID
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Chama a função CRUD para atualizar o cliente
    return crud.update_customer(db, db_customer=db_customer, customer=customer)