FROM python:3.11

WORKDIR /app

COPY backend/mcps/activities/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/mcps/activities/ .
COPY firebase/ ./firebase

EXPOSE 3001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]