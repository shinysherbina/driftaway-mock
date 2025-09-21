FROM python:3.11

WORKDIR /app
ENV PYTHONPATH=/app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure Python can resolve local packages
ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 4000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]