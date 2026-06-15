FROM python:3.11-slim

WORKDIR /app

COPY laboratory_work_7/parser/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY laboratory_work_7/parser/main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
