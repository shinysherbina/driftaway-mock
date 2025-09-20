FROM python:3.11

WORKDIR /app

COPY backend/mcps/local_transport/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/mcps/local_transport/ .
COPY firebase/ ./firebase

EXPOSE 3007

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3007"]