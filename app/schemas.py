from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Literal
from .models import OpportunityStage

# ----- Customers -----
class CustomerBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=150)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None

class CustomerOut(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ----- Interactions -----
class InteractionBase(BaseModel):
    type: str
    notes: Optional[str] = None
    occurred_at: Optional[datetime] = None

class InteractionCreate(InteractionBase):
    pass

class InteractionOut(InteractionBase):
    id: int
    customer_id: int

    class Config:
        from_attributes = True

# ----- Opportunities -----
class OpportunityBase(BaseModel):
    title: str
    stage: OpportunityStage = OpportunityStage.new
    value: Optional[float] = None
    close_date: Optional[datetime] = None

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    stage: Optional[OpportunityStage] = None
    value: Optional[float] = None
    close_date: Optional[datetime] = None

class OpportunityOut(OpportunityBase):
    id: int
    customer_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ----- Users  -----


class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

