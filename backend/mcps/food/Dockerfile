FROM python:3.11

WORKDIR /app

COPY backend/mcps/food/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/mcps/food/ .
COPY firebase/ ./firebase

EXPOSE 3004

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3004"]