# Лабораторная работа 1 (II семестр)

## Тема
Реализация серверного приложения FastAPI.

## Выбранная тема
Программа-тайм-менеджер.

## Цель работы
Реализовать серверное приложение на FastAPI с PostgreSQL, SQLAlchemy, Alembic и авторизацией по JWT.

## Практики 1.1–1.3

| Практика | Файлы |
|---|---|
| 1.1 | `app/database.py`, `app/models.py`, `alembic/` |
| 1.2 | `app/schemas.py`, `app/main.py` |
| 1.3 | `app/auth.py` |

## Модель данных

6 таблиц: `users`, `projects`, `tasks`, `tags`, `task_tags`, `time_entries`.

Связи:
- one-to-many: пользователь → проекты, проект → задачи, задача → записи времени
- many-to-many: задачи ↔ теги через `task_tags`
- у `task_tags` есть поля `relation_note` и `assigned_at`

## Соединение с базой данных

```python
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/time_manager",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
```

## Авторизация

- регистрация и вход
- JWT-токен создаётся вручную в `app/auth.py`
- хэш пароля через `hashlib.pbkdf2_hmac`

```text
Authorization: Bearer <access_token>
```

## Эндпоинты

### Авторизация и пользователи
- `POST /auth/register`
- `POST /auth/login`
- `GET /users/me`
- `GET /users`
- `POST /users/change-password`

### Проекты
- `GET /projects`
- `POST /projects`
- `GET /projects/{project_id}` — со списком задач
- `PUT /projects/{project_id}`
- `DELETE /projects/{project_id}`

### Задачи
- `GET /tasks`
- `POST /tasks`
- `GET /tasks/{task_id}` — с тегами и записями времени
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

### Теги
- `GET /tags`
- `POST /tags`
- `GET /tags/{tag_id}`
- `PUT /tags/{tag_id}`
- `DELETE /tags/{tag_id}`
- `POST /tasks/{task_id}/tags`
- `DELETE /tasks/{task_id}/tags/{tag_id}`

### Учёт времени
- `POST /tasks/{task_id}/time-entries`
- `GET /tasks/{task_id}/time-entries`
- `PUT /time-entries/{entry_id}`
- `DELETE /time-entries/{entry_id}`

## Запуск

```bash
cd laboratory_work_5
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/time_manager"
export SECRET_KEY="local-secret-key"
alembic upgrade head
uvicorn app.main:app --reload
```

## Вывод

Реализовано FastAPI-приложение тайм-менеджера с CRUD, вложенными объектами и JWT-авторизацией.
