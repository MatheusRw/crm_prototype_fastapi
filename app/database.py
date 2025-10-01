from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# Configuração para Cloud SQL
def get_database_url():
    # Para desenvolvimento local, use SQLite
    if os.getenv("ENVIRONMENT") == "development" or not os.getenv("DATABASE_URL"):
        return "sqlite:///./app.db"
    
    # Para produção (Cloud SQL)
    return os.getenv(
        "DATABASE_URL", 
        "postgresql+psycopg2://username:password@localhost/crm"
    )

# Criar engine
DATABASE_URL = get_database_url()

# Configurações diferentes para SQLite vs PostgreSQL
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
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