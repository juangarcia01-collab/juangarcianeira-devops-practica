FROM python:3.12-slim

WORKDIR /app

# dependencias (versiones fijadas en requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# codigo fuente de la Practica 2
COPY src/ src/

# usuario sin privilegios: evita correr la app como root dentro del contenedor
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app
USER appuser

WORKDIR /app/src

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
