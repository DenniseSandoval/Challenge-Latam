FROM python:3.11.4

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos al directorio de trabajo
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
