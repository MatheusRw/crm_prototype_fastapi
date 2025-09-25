from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
import os

# Configuração para Cloud SQL
def get_database_url():
    # URL para Cloud SQL via Unix socket
    return os.getenv(
        "DATABASE_URL", 
        "postgresql+psycopg2://postgres:senha123@/crm?host=/cloudsql/crm-matheus:southamerica-east1:crm-db"
    )

# Criar engine
DATABASE_URL = get_database_url()
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()