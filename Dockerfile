FROM python:3.10-slim

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalación robusta de dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalamos las librerías de Python
RUN pip install --no-cache-dir gradio==4.44.1 gradio_client==1.3.0 pillow

COPY . .

# Exponemos el puerto de Gradio
EXPOSE 7860

CMD ["python", "app.py"]
