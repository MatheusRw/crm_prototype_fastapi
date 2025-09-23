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

# Copiar código da aplicação
COPY app/ .

# Expor porta
EXPOSE 8080

# Comando de inicialização
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]