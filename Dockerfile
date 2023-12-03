FROM python:3.11.4
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "challenge.api:app", "--host", "127.0.0.1", "--port", "8000"]
