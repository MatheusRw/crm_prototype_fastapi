from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import Base, engine, get_db
from app import models, schemas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CRM Simples", version="0.1.0")

# Cria as tabelas automaticamente
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend funcionando"}

# ============================================
# AUTH SIMPLIFICADA - SEM NAME
# ============================================
@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    """Login SIMPLES - sem hash complexo"""
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Email não encontrado")
    
    # ✅ Comparação direta (sem hash para testes)
    if user.hashed_password != password:
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    # ✅ Token simples
    access_token = f"user-token-{user.id}"
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.id
    }

@app.post("/create-test-user")
def create_test_user(db: Session = Depends(get_db)):
    """Cria usuário de teste - SEM NAME"""
    existing_user = db.query(models.User).filter(models.User.email == "teste@crm.com").first()
    if existing_user:
        return {"message": "Usuário já existe", "user_id": existing_user.id}
    
    user = models.User(
        email="teste@crm.com",
        hashed_password="123456",  # Senha em texto puro
        is_active=True
        # ✅ SEM name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Usuário de teste criado", "user_id": user.id}

# ============================================
# CUSTOMERS (mantenha suas rotas existentes)
# ============================================
@app.post("/customers", response_model=schemas.CustomerOut, status_code=201)
def create_customer(payload: schemas.CustomerCreate, db: Session = Depends(get_db)):
    if payload.email:
        existing = db.query(models.Customer).filter(models.Customer.email == payload.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
    
    db_customer = models.Customer(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        company=payload.company
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customers", response_model=List[schemas.CustomerOut])
def list_customers(
    q: Optional[str] = Query(default=None, description="Busca por nome/email/empresa"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(models.Customer)
    if q:
        query = query.filter(
            models.Customer.name.ilike(f"%{q}%") |
            models.Customer.email.ilike(f"%{q}%") |
            models.Customer.company.ilike(f"%{q}%")
        )
    return query.offset(offset).limit(limit).all()

@app.get("/customers/{customer_id}", response_model=schemas.CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer

# ============================================
# OPPORTUNITIES (mantenha suas rotas existentes)
# ============================================
@app.post("/customers/{customer_id}/opportunities", response_model=schemas.OpportunityOut, status_code=201)
def create_opportunity(customer_id: int, payload: schemas.OpportunityCreate, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    db_opportunity = models.Opportunity(
        customer_id=customer_id,
        title=payload.title,
        stage=payload.stage,
        value=payload.value,
        close_date=payload.close_date
    )
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity

@app.get("/opportunities", response_model=List[schemas.OpportunityOut])
def list_all_opportunities(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    return db.query(models.Opportunity).offset(offset).limit(limit).all()

# ============================================
# USERS (simplificado)
# ============================================
@app.post("/users", response_model=schemas.UserOut)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    user = models.User(
        email=payload.email,
        hashed_password=payload.password,  # Texto puro para testes
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users", response_model=List[schemas.UserOut])
def list_users(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    return db.query(models.User).offset(offset).limit(limit).all()

# Startup event
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas do PostgreSQL criadas/validadas")