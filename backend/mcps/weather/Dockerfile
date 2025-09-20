FROM python:3.11

WORKDIR /app

COPY backend/mcps/weather/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/mcps/weather/ .
COPY firebase/ ./firebase

EXPOSE 3011

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3011"]