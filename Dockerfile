FROM python:3.11-slim

# Evitar pyc y buffering
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instalar dependencias del sistema (pueden ser necesarias para gRPC de Google Cloud)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY app /app

# Variables de entorno por defecto
ENV HOST=0.0.0.0
ENV PORT=8080

# Ejecutar servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
