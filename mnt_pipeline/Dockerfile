# -----------------------
# AutoSAGE ML Dockerfile
# -----------------------

FROM python:3.11-slim

# Atualiza pacotes essenciais
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Diretório da aplicação
WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY src ./src

# 🔥 ADICIONE ISSO (CRÍTICO)
ENV PYTHONPATH=/app

# Expor porta da API
EXPOSE 9000

# Comando para iniciar o ML
CMD ["python", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "9000"]
