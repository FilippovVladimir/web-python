# Лабораторная работа 7. Docker, FastAPI, Parser Service, Celery и Redis

## 1. Цель работы

Цель работы - упаковать приложение и связанные сервисы в Docker, вынести парсер в отдельный сервис, реализовать вызов парсера из основного API и добавить асинхронную обработку задач через Celery и Redis.

В работе используются:

- Docker
- Docker Compose
- FastAPI
- PostgreSQL
- Redis
- Celery
- Celery Beat
- отдельный parser service
- HTTP-взаимодействие между сервисами

## 2. Общая архитектура

В проекте есть несколько сервисов:

| Сервис | Назначение |
|---|---|
| `db` | PostgreSQL база данных |
| `redis` | брокер сообщений для Celery |
| `api` | основное FastAPI-приложение |
| `parser` | отдельный сервис для парсинга страниц |
| `celery_worker` | выполняет фоновые задачи |
| `celery_beat` | запускает периодические задачи |

Сервисы запускаются вместе через Docker Compose.

## 3. Структура проекта

```text
laboratory_work_7/
├── api/
│   └── Dockerfile
├── parser/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── docker-compose.yml
```

Также для ЛР7 используются файлы из ЛР5:

```text
laboratory_work_5/app/parse_routes.py
laboratory_work_5/app/celery_app.py
laboratory_work_5/app/tasks.py
laboratory_work_5/app/main.py
```

## 4. Docker Compose

Главный файл запуска:

```text
laboratory_work_7/docker-compose.yml
```

Что искать:

```yaml
services:
```

```yaml
db:
```

```yaml
redis:
```

```yaml
parser:
```

```yaml
api:
```

```yaml
celery_worker:
```

```yaml
celery_beat:
```

Docker Compose описывает, какие контейнеры нужно создать, как они связаны между собой и какие переменные окружения используются.

## 5. Сервис db

Сервис `db` запускает PostgreSQL.

Назначение:

- хранить данные приложения;
- хранить результаты парсинга;
- быть общей базой для API и parser service.

Что сказать:

> PostgreSQL запущен как отдельный контейнер. Остальные сервисы подключаются к нему по имени сервиса `db`.

Внутри Docker Compose сервисы обращаются друг к другу не через `localhost`, а по имени сервиса. Например:

```text
db:5432
```

## 6. Сервис redis

Redis используется как брокер сообщений для Celery.

Назначение:

- принимать задачи от FastAPI;
- передавать задачи worker-у;
- хранить состояние выполнения задач.

Что сказать:

> Redis нужен для очереди задач. FastAPI кладет задачу в Redis, а Celery worker забирает ее и выполняет.

## 7. Сервис api

Сервис `api` - это основное FastAPI-приложение.

Dockerfile:

```text
laboratory_work_7/api/Dockerfile
```

Что искать:

```dockerfile
FROM python:3.11-slim
```

```dockerfile
CMD
```

Что делает Dockerfile:

1. Создает Python-окружение внутри контейнера.
2. Устанавливает зависимости.
3. Копирует приложение.
4. Применяет миграции Alembic.
5. Запускает FastAPI через Uvicorn.

Что сказать:

> API-контейнер запускает основное FastAPI-приложение, применяет миграции и открывает Swagger-документацию.

## 8. Сервис parser

Parser service - отдельный FastAPI-сервис для парсинга веб-страниц.

Файл:

```text
laboratory_work_7/parser/main.py
```

Что искать:

```python
@app.post("/parse")
```

Как работает:

1. Parser service принимает URL.
2. Делает HTTP-запрос к странице.
3. Извлекает `title`.
4. Сохраняет результат в базу данных.
5. Возвращает JSON с результатом.

Что сказать:

> Парсер вынесен в отдельный сервис. Основное API не парсит страницу напрямую, а вызывает parser service по HTTP.

## 9. Dockerfile parser service

Файл:

```text
laboratory_work_7/parser/Dockerfile
```

Что искать:

```dockerfile
CMD ["uvicorn", "main:app"
```

Что делает:

- устанавливает зависимости парсера;
- копирует код;
- запускает FastAPI-приложение парсера через Uvicorn.

Parser service обычно доступен снаружи по адресу:

```text
http://127.0.0.1:8001/docs
```

Внутри Docker-сети API обращается к нему по адресу:

```text
http://parser:8000
```

## 10. Вызов parser service из API

Файл:

```text
laboratory_work_5/app/parse_routes.py
```

Что искать:

```python
@router.post("/sync")
```

```python
@router.post("/async")
```

```python
@router.get("/status/{task_id}")
```

### Синхронный вызов

Endpoint:

```text
POST /parse/sync
```

Как работает:

1. Клиент отправляет URL в основной API.
2. Основной API через HTTP вызывает parser service.
3. Parser service парсит страницу.
4. Основной API возвращает клиенту результат.

Что сказать:

> В синхронном варианте API ждет, пока parser service завершит парсинг, и сразу возвращает результат.

### Асинхронный вызов

Endpoint:

```text
POST /parse/async
```

Как работает:

1. Клиент отправляет URL.
2. API не выполняет парсинг сразу.
3. API ставит задачу в очередь Celery.
4. Клиент сразу получает `task_id`.
5. По `task_id` можно проверить статус задачи.

Что сказать:

> В асинхронном варианте API не блокируется. Он возвращает task_id, а парсинг выполняется Celery worker-ом в фоне.

### Проверка статуса

Endpoint:

```text
GET /parse/status/{task_id}
```

Как работает:

1. Клиент передает `task_id`.
2. API проверяет состояние задачи в Celery.
3. Возвращает статус: pending, success, failure и результат, если он есть.

## 11. Celery

Celery используется для фоновых задач.

Основной файл:

```text
laboratory_work_5/app/celery_app.py
```

Что искать:

```python
celery_app = Celery
```

```python
broker
```

```python
backend
```

Как работает:

- Redis используется как broker;
- Redis используется как backend;
- worker получает задачи из очереди;
- beat может запускать задачи по расписанию.

Что сказать:

> Celery позволяет выполнять тяжелые или долгие задачи в фоне, чтобы HTTP-запрос не ждал завершения операции.

## 12. Celery task

Файл:

```text
laboratory_work_5/app/tasks.py
```

Что искать:

```python
def parse_url_task
```

Как работает:

1. Celery worker получает задачу.
2. Выполняет HTTP-запрос к parser service.
3. Возвращает результат в Celery backend.

Что сказать:

> Задача `parse_url_task` выполняется не в основном API, а в отдельном Celery worker-е.

## 13. Celery Beat

Celery Beat запускает задачи по расписанию.

Где искать:

```text
laboratory_work_5/app/celery_app.py
```

Что искать:

```python
beat_schedule
```

Что сказать:

> Celery Beat нужен для периодических задач. Например, можно регулярно запускать парсинг определенного URL.

## 14. Запуск ЛР7

Перейти в папку:

```bash
cd laboratory_work_7
```

Запустить все сервисы:

```bash
docker compose up --build
```

Если используется старая версия Docker Compose:

```bash
docker-compose up --build
```

После запуска открыть:

Основное API:

```text
http://127.0.0.1:8000/docs
```

Parser service:

```text
http://127.0.0.1:8001/docs
```

## 15. Проверка работы

### 15.1 Проверка parser service

Открыть:

```text
http://127.0.0.1:8001/docs
```

Выполнить:

```text
POST /parse
```

Пример тела запроса:

```json
{
  "url": "https://example.com"
}
```

Ожидаемый результат:

- URL;
- title страницы;
- статус успешного выполнения.

### 15.2 Проверка синхронного парсинга через API

Открыть:

```text
http://127.0.0.1:8000/docs
```

Выполнить:

```text
POST /parse/sync
```

Пример:

```json
{
  "url": "https://example.com"
}
```

Что должно произойти:

- API вызовет parser service;
- parser service вернет результат;
- API отдаст результат клиенту.

### 15.3 Проверка асинхронного парсинга

Выполнить:

```text
POST /parse/async
```

Пример:

```json
{
  "url": "https://example.com"
}
```

Ответ должен содержать:

```json
{
  "task_id": "..."
}
```

Затем выполнить:

```text
GET /parse/status/{task_id}
```

Если задача выполнена, будет возвращен результат.

## 16. Что показывать на защите

Минимальный план демонстрации:

1. Открыть `docker-compose.yml`.
2. Показать сервисы `db`, `redis`, `api`, `parser`, `celery_worker`, `celery_beat`.
3. Запустить:

```bash
docker compose up --build
```

4. Открыть:

```text
http://127.0.0.1:8000/docs
```

5. Показать `POST /parse/sync`.
6. Показать `POST /parse/async`.
7. Показать `GET /parse/status/{task_id}`.
8. Открыть код parser service:
   - `laboratory_work_7/parser/main.py`
9. Открыть код Celery:
   - `laboratory_work_5/app/celery_app.py`
   - `laboratory_work_5/app/tasks.py`

## 17. Что сказать про Docker

> Docker нужен, чтобы запускать каждую часть приложения в отдельном контейнере. Это упрощает настройку окружения и делает запуск проекта одинаковым на разных компьютерах.

## 18. Что сказать про Docker Compose

> Docker Compose запускает сразу несколько контейнеров одной командой. В этой работе через Compose поднимаются API, PostgreSQL, Redis, parser service, Celery worker и Celery Beat.

## 19. Что сказать про Redis

> Redis используется как очередь задач для Celery. API кладет задачу в Redis, worker забирает ее и выполняет.

## 20. Что сказать про Celery

> Celery нужен для фонового выполнения задач. Благодаря этому долгий парсинг не блокирует основной HTTP-запрос.

## 21. Возможная проблема с depends_on

В Docker Compose `depends_on` гарантирует порядок запуска контейнеров, но не всегда гарантирует, что база данных уже полностью готова принимать подключения.

Что сказать, если спросят:

> В учебной версии используется `depends_on`. Для более надежного production-запуска можно добавить healthcheck для PostgreSQL и запускать API только после готовности базы.

## 22. Краткий вывод

В лабораторной работе приложение было развернуто через Docker Compose. Основное FastAPI-приложение, PostgreSQL, Redis, parser service, Celery worker и Celery Beat запускаются как отдельные сервисы. Реализован синхронный HTTP-вызов парсера и асинхронная постановка задачи в очередь через Celery.
