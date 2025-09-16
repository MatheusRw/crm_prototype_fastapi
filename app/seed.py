# seed.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # adiciona a raiz

from app.database import SessionLocal, Base, engine
from app import models

# Cria tabelas
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Criar clientes de exemplo
cliente1 = models.Customer(name="João Silva", email="joao@example.com", phone="11999999999")
cliente2 = models.Customer(name="Maria Souza", email="maria@example.com", phone="11988888888")
db.add_all([cliente1, cliente2])
db.commit()

# Criar algumas oportunidades
opp1 = models.Opportunity(customer_id=cliente1.id, title="Venda Software", value=5000)
opp2 = models.Opportunity(customer_id=cliente2.id, title="Consultoria TI", value=3000)
db.add_all([opp1, opp2])
db.commit()

db.close()

print("Banco populado com dados de teste ✅")
