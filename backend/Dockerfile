FROM node:18-slim AS frontend-build

WORKDIR /frontend

# Copiar e instalar dependências do frontend
COPY ../frontend/package*.json ./
RUN npm ci

# Copiar código do frontend e fazer build
COPY ../frontend/ ./
RUN npm run build

# Stage 2: Python backend
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema necessárias para PyMuPDF
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do backend
COPY . .

# Copiar build do frontend do stage anterior
COPY --from=frontend-build /frontend/dist ../frontend/dist

# Expor porta
EXPOSE 8080

# Comando de inicialização
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

