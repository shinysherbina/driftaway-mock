FROM python:3.11

WORKDIR /app

COPY backend/mcps/hotel/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/mcps/hotel/ .
COPY firebase/ ./firebase

EXPOSE 3006

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3006"]