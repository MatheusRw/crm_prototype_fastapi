from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from typing import Sequence, Optional
from passlib.context import CryptContext


from . import models, schemas

# ----- Customers -----
def create_customer(db: Session, data: schemas.CustomerCreate):
    customer = models.Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def list_customers(db: Session, q: Optional[str] = None, limit: int = 50, offset: int = 0) -> Sequence[models.Customer]:
    stmt = select(models.Customer).order_by(desc(models.Customer.created_at)).limit(limit).offset(offset)
    if q:
        q_like = f"%{q.lower()}%"
        stmt = select(models.Customer).where(
            (models.Customer.name.ilike(q_like)) |
            (models.Customer.email.ilike(q_like)) |
            (models.Customer.company.ilike(q_like))
        ).order_by(desc(models.Customer.created_at)).limit(limit).offset(offset)
    return db.scalars(stmt).all()

def get_customer(db: Session, customer_id: int) -> Optional[models.Customer]:
    return db.get(models.Customer, customer_id)

def update_customer(db: Session, customer_id: int, data: schemas.CustomerUpdate) -> Optional[models.Customer]:
    customer = db.get(models.Customer, customer_id)
    if not customer:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(customer, k, v)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def delete_customer(db: Session, customer_id: int) -> bool:
    customer = db.get(models.Customer, customer_id)
    if not customer:
        return False
    db.delete(customer)
    db.commit()
    return True

# ----- Interactions -----
def create_interaction(db: Session, customer_id: int, data: schemas.InteractionCreate) -> models.Interaction:
    interaction = models.Interaction(customer_id=customer_id, **data.model_dump())
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction

def list_interactions(db: Session, customer_id: int, limit: int = 100, offset: int = 0):
    stmt = select(models.Interaction).where(models.Interaction.customer_id == customer_id).order_by(
        desc(models.Interaction.occurred_at)
    ).limit(limit).offset(offset)
    return db.scalars(stmt).all()

def delete_interaction(db: Session, interaction_id: int) -> bool:
    interaction = db.get(models.Interaction, interaction_id)
    if not interaction:
        return False
    db.delete(interaction)
    db.commit()
    return True

# ----- Opportunities -----
def create_opportunity(db: Session, customer_id: int, data: schemas.OpportunityCreate) -> models.Opportunity:
    opp = models.Opportunity(customer_id=customer_id, **data.model_dump())
    db.add(opp)
    db.commit()
    db.refresh(opp)
    return opp

def list_opportunities(db: Session, customer_id: int, limit: int = 100, offset: int = 0):
    stmt = select(models.Opportunity).where(models.Opportunity.customer_id == customer_id).order_by(
        desc(models.Opportunity.created_at)
    ).limit(limit).offset(offset)
    return db.scalars(stmt).all()

def update_opportunity(db: Session, opportunity_id: int, data: schemas.OpportunityUpdate):
    opp = db.get(models.Opportunity, opportunity_id)
    if not opp:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(opp, k, v)
    db.add(opp)
    db.commit()
    db.refresh(opp)
    return opp

def delete_opportunity(db: Session, opportunity_id: int) -> bool:
    opp = db.get(models.Opportunity, opportunity_id)
    if not opp:
        return False
    db.delete(opp)
    db.commit()
    return True

# ----- Users  -----

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, data: schemas.UserCreate):
    hashed_password = pwd_context.hash(data.password)
    user = models.User(email=data.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ----- Users -----

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()



#------- Criando as lista dos usuarios e das oportunidades

# Opportunities
def list_all_opportunities(db: Session, limit: int = 100, offset: int = 0):
    return db.query(models.Opportunity).offset(offset).limit(limit).all()


# Users
def list_users(db: Session, limit: int = 100, offset: int = 0):
    return db.query(models.User).offset(offset).limit(limit).all()





#atualiza usuario 
def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None

    # Atualiza apenas os campos enviados
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Função para atualizar um cliente
def update_customer(db: Session, customer_id: int, customer: schemas.CustomerCreate):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    for key, value in customer.dict().items():
        setattr(db_customer, key, value)
    
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer