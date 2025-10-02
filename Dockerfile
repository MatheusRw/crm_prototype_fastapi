FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ CORREÇÃO: Copiar toda a estrutura do projeto
COPY . .

# ✅ CORREÇÃO: Comando correto - main.py está em app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

# Expor porta
EXPOSE 8080