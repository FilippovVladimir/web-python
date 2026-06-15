# Лабораторная работа 3 (II семестр)

## Цель
Упаковать FastAPI, PostgreSQL и парсер в Docker, вызвать парсер по HTTP и через Celery + Redis.

## Архитектура

| Сервис | Порт | Описание |
|---|---|---|
| api | 8000 | FastAPI из ЛР5 |
| parser | 8001 | сервис парсера |
| db | 5432 | PostgreSQL |
| redis | 6379 | брокер Celery |
| celery_worker | — | фоновые задачи |
| celery_beat | — | периодический парсинг |

## Подзадача 1. Docker

- FastAPI: `laboratory_work_5`
- Парсер: `laboratory_work_7/parser/main.py`
- Dockerfile: `laboratory_work_7/api/Dockerfile`, `laboratory_work_7/parser/Dockerfile`
- Оркестрация: `laboratory_work_7/docker-compose.yml`

```python
@app.post("/parse")
def parse(data: ParseRequest) -> dict:
    response = requests.get(data.url, timeout=15)
    response.raise_for_status()
    title = extract_title(response.text)
    save_page(data.url, title)
    return {"message": "Parsing completed", "url": data.url, "title": title}
```

## Подзадача 2. Вызов парсера из API

| Метод | URL | Описание |
|---|---|---|
| POST | `/parse/sync` | синхронный вызов парсера |
| POST | `/parse/async` | постановка задачи в очередь |
| GET | `/parse/status/{task_id}` | статус задачи |

## Подзадача 3. Celery + Redis

- `app/celery_app.py` — конфигурация Celery
- `app/tasks.py` — задача `parse_url_task`
- Celery Beat парсит `https://example.com` каждый час

## Запуск

```bash
cd laboratory_work_7
docker compose up --build
```

## Примеры запросов

```bash
curl -X POST "http://localhost:8001/parse" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'

curl -X POST "http://localhost:8000/parse/sync" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'

curl -X POST "http://localhost:8000/parse/async" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://python.org"}'
```

## Вывод

Приложение, база данных и парсер работают в Docker. Парсер вызывается синхронно через HTTP и асинхронно через Celery + Redis.
