FROM python:3.11-slim

WORKDIR /app

COPY laboratory_work_5/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY laboratory_work_5/alembic.ini .
COPY laboratory_work_5/alembic ./alembic
COPY laboratory_work_5/app ./app

ENV PYTHONPATH=/app

EXPOSE 8000

CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
