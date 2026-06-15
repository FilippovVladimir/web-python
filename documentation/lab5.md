# Лабораторная работа 5. Серверное приложение на FastAPI

## 1. Цель работы

Цель работы - реализовать серверное приложение на FastAPI с использованием PostgreSQL, SQLAlchemy, Alembic, Pydantic-схем, CRUD-методов и JWT-аутентификации.

В качестве предметной области выбрано приложение для тайм-менеджмента. Система позволяет пользователю создавать проекты, задачи, назначать задачам теги и фиксировать затраченное время.

## 2. Используемые технологии

В работе используются:

- Python 3.10+
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Alembic
- Pydantic
- Uvicorn
- Docker для запуска PostgreSQL
- JWT-аутентификация, реализованная вручную
- хэширование паролей через `hashlib`

## 3. Структура проекта

Основные файлы лабораторной работы:

```text
laboratory_work_5/
├── alembic/
│   ├── versions/
│   └── env.py
├── app/
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── parse_routes.py
│   ├── schemas.py
│   ├── celery_app.py
│   └── tasks.py
├── alembic.ini
├── requirements.txt
├── .env.example
└── .env
```

Назначение основных файлов:

| Файл | Назначение |
|---|---|
| `app/main.py` | Основные endpoint-ы FastAPI |
| `app/models.py` | ORM-модели SQLAlchemy |
| `app/schemas.py` | Pydantic-схемы запросов и ответов |
| `app/database.py` | Подключение к PostgreSQL |
| `app/auth.py` | JWT, хэширование паролей, получение текущего пользователя |
| `alembic/` | Миграции базы данных |
| `alembic.ini` | Конфигурация Alembic |

## 4. Модель данных

В приложении реализовано 6 таблиц:

1. `users` - пользователи
2. `projects` - проекты
3. `tasks` - задачи
4. `tags` - теги
5. `task_tags` - ассоциативная таблица для связи задач и тегов
6. `time_entries` - записи затраченного времени

Файл с моделями:

```text
laboratory_work_5/app/models.py
```

## 5. Описание таблиц

### 5.1 User

Модель `User` хранит данные пользователя.

Основные поля:

- `id`
- `username`
- `email`
- `hashed_password`

Пользователь может иметь много проектов и много задач.

Фрагмент для поиска в коде:

```python
class User(Base):
```

### 5.2 Project

Модель `Project` хранит проекты пользователя.

Основные поля:

- `id`
- `name`
- `description`
- `owner_id`

Каждый проект принадлежит одному пользователю. Один пользователь может иметь много проектов.

Фрагмент для поиска:

```python
class Project(Base):
```

### 5.3 Task

Модель `Task` хранит задачи.

Основные поля:

- `id`
- `title`
- `description`
- `deadline`
- `priority`
- `status`
- `project_id`
- `user_id`

Задача принадлежит проекту и пользователю. У задачи могут быть теги и записи времени.

Фрагмент для поиска:

```python
class Task(Base):
```

### 5.4 Tag

Модель `Tag` хранит теги.

Основные поля:

- `id`
- `name`

Теги используются для группировки задач.

Фрагмент для поиска:

```python
class Tag(Base):
```

### 5.5 TaskTag

Модель `TaskTag` реализует связь many-to-many между задачами и тегами.

Основные поля:

- `task_id`
- `tag_id`
- `relation_note`
- `assigned_at`

Важно: ассоциативная сущность содержит дополнительные поля `relation_note` и `assigned_at`. Это соответствует требованию задания: связь many-to-many должна иметь поле, характеризующее связь, кроме ссылок на связанные таблицы.

Фрагмент для поиска:

```python
class TaskTag(Base):
```

### 5.6 TimeEntry

Модель `TimeEntry` хранит записи затраченного времени.

Основные поля:

- `id`
- `task_id`
- `minutes`
- `comment`
- `created_at`

Одна задача может иметь много записей времени.

Фрагмент для поиска:

```python
class TimeEntry(Base):
```

## 6. Связи между таблицами

### One-to-many

В работе есть несколько связей один-ко-многим:

| Связь | Описание |
|---|---|
| `User -> Project` | один пользователь имеет много проектов |
| `User -> Task` | один пользователь имеет много задач |
| `Project -> Task` | один проект содержит много задач |
| `Task -> TimeEntry` | одна задача имеет много записей времени |

В коде связи реализованы через `ForeignKey` и `relationship`.

Что найти в коде:

```python
ForeignKey
```

```python
relationship
```

### Many-to-many

Связь many-to-many реализована между задачами и тегами:

```text
Task <-> TaskTag <-> Tag
```

Таблица `task_tags` является ассоциативной сущностью.

Что найти в коде:

```python
class TaskTag(Base):
```

## 7. Подключение к базе данных

Подключение к PostgreSQL находится в файле:

```text
laboratory_work_5/app/database.py
```

В этом файле задается `DATABASE_URL`, создается `engine`, `SessionLocal` и базовый класс `Base`.

Ключевые фрагменты для поиска:

```python
DATABASE_URL
```

```python
create_engine
```

```python
SessionLocal
```

```python
get_db
```

Функция `get_db()` используется в endpoint-ах через `Depends`. Она создает сессию базы данных, передает ее в обработчик запроса и закрывает после выполнения.

Пример строки подключения:

```env
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/time_manager
SECRET_KEY=secret-key
```

Если PostgreSQL запущен через Docker на порту `5433`, то в `DATABASE_URL` также должен быть указан порт `5433`.

## 8. Миграции Alembic

Для управления структурой базы данных используется Alembic.

Основные файлы:

```text
laboratory_work_5/alembic/
laboratory_work_5/alembic.ini
```

Команда применения миграций:

```bash
alembic upgrade head
```

Что сказать:

> Alembic нужен, чтобы создавать и изменять таблицы базы данных через миграции, а не вручную.

## 9. Pydantic-схемы

Pydantic-схемы находятся в файле:

```text
laboratory_work_5/app/schemas.py
```

Схемы нужны для:

- описания тела входящих запросов;
- проверки типов;
- описания структуры ответа;
- автоматической генерации Swagger-документации.

Примеры схем:

```python
class UserCreate(BaseModel):
```

```python
class ProjectCreate(BaseModel):
```

```python
class TaskCreate(BaseModel):
```

```python
class TaskDetail(TaskRead):
```

Схемы `Create` используются для создания объектов. Схемы `Read` используются для ответа API. Схемы `Detail` могут возвращать вложенные данные.

## 10. Авторизация и регистрация

В работе реализован пользовательский функционал:

- регистрация;
- вход;
- генерация JWT-токена;
- проверка JWT-токена;
- получение текущего пользователя;
- список пользователей;
- смена пароля;
- хэширование паролей.

Основные файлы:

```text
laboratory_work_5/app/main.py
laboratory_work_5/app/auth.py
```

### Регистрация

Endpoint:

```text
POST /auth/register
```

Где искать:

```python
@app.post("/auth/register"
```

Как работает:

1. Пользователь отправляет `username`, `email`, `password`.
2. Сервер проверяет, нет ли такого пользователя.
3. Пароль хэшируется.
4. Пользователь сохраняется в базе.

Пример тела запроса:

```json
{
  "username": "user1",
  "email": "user1@mail.com",
  "password": "12345678"
}
```

### Вход

Endpoint:

```text
POST /auth/login
```

Где искать:

```python
@app.post("/auth/login"
```

Как работает:

1. Пользователь отправляет логин и пароль.
2. Сервер ищет пользователя.
3. Пароль проверяется через `verify_password`.
4. Если данные верные, сервер возвращает JWT-токен.

Пример тела запроса:

```json
{
  "username": "user1",
  "password": "12345678"
}
```

### Получение текущего пользователя

Endpoint:

```text
GET /users/me
```

Где искать:

```python
@app.get("/users/me"
```

Этот endpoint защищен. Для его вызова нужно передать JWT-токен в заголовке:

```text
Authorization: Bearer <token>
```

## 11. JWT

JWT реализован в файле:

```text
laboratory_work_5/app/auth.py
```

Основные функции:

```python
def create_access_token
```

```python
def decode_access_token
```

```python
def get_current_user
```

Как работает JWT:

1. После логина сервер создает токен.
2. В токен записывается имя пользователя и срок действия.
3. Токен подписывается секретным ключом.
4. Клиент отправляет токен в заголовке `Authorization`.
5. Сервер проверяет подпись и срок действия токена.

JWT сделан вручную: формируется header, payload и подпись.

## 12. Хэширование паролей

Хэширование находится в файле:

```text
laboratory_work_5/app/auth.py
```

Что искать:

```python
def hash_password
```

```python
def verify_password
```

Как работает:

- `hash_password()` создает соль и хэширует пароль.
- `verify_password()` повторяет хэширование введенного пароля и сравнивает результат с сохраненным хэшем.

Пароли не хранятся в базе в открытом виде.

## 13. CRUD-методы

В приложении реализованы CRUD-операции для основных сущностей.

### Projects

Endpoint-ы:

| Метод | URL | Назначение |
|---|---|---|
| GET | `/projects` | получить список проектов |
| POST | `/projects` | создать проект |
| GET | `/projects/{project_id}` | получить один проект |
| PUT | `/projects/{project_id}` | обновить проект |
| DELETE | `/projects/{project_id}` | удалить проект |

Где искать:

```python
@app.get("/projects"
```

```python
@app.post("/projects"
```

```python
@app.put("/projects/{project_id}"
```

```python
@app.delete("/projects/{project_id}"
```

### Tasks

Endpoint-ы:

| Метод | URL | Назначение |
|---|---|---|
| GET | `/tasks` | получить список задач |
| POST | `/tasks` | создать задачу |
| GET | `/tasks/{task_id}` | получить задачу |
| PUT | `/tasks/{task_id}` | обновить задачу |
| DELETE | `/tasks/{task_id}` | удалить задачу |

### Tags

Endpoint-ы:

| Метод | URL | Назначение |
|---|---|---|
| GET | `/tags` | получить список тегов |
| POST | `/tags` | создать тег |
| GET | `/tags/{tag_id}` | получить тег |
| PUT | `/tags/{tag_id}` | обновить тег |
| DELETE | `/tags/{tag_id}` | удалить тег |

### TaskTag

Endpoint-ы:

| Метод | URL | Назначение |
|---|---|---|
| POST | `/tasks/{task_id}/tags` | добавить тег к задаче |
| DELETE | `/tasks/{task_id}/tags/{tag_id}` | удалить тег у задачи |

### TimeEntry

Endpoint-ы:

| Метод | URL | Назначение |
|---|---|---|
| POST | `/tasks/{task_id}/time-entries` | добавить запись времени |
| GET | `/tasks/{task_id}/time-entries` | получить записи времени задачи |
| PUT | `/time-entries/{entry_id}` | обновить запись времени |
| DELETE | `/time-entries/{entry_id}` | удалить запись времени |

## 14. Вложенные объекты

В задании требуется возвращать модели с вложенными объектами там, где это необходимо.

В проекте для этого используется `selectinload`.

Что искать в коде:

```python
selectinload(Project.tasks)
```

```python
selectinload(Task.tag_links)
```

```python
selectinload(Task.time_entries)
```

Пример:

- при получении проекта можно вернуть проект со списком задач;
- при получении задачи можно вернуть связанные теги и записи времени.

## 15. Запуск проекта

### 15.1 Запуск PostgreSQL через Docker

Если порт `5432` занят, можно использовать порт `5433`:

```bash
docker run --name time_manager_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=time_manager \
  -p 5433:5432 \
  -d postgres:15
```

Проверка:

```bash
docker ps
```

### 15.2 Создание `.env`

В папке `laboratory_work_5`:

```bash
cat > .env << 'EOF'
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/time_manager
SECRET_KEY=secret-key
EOF
```

### 15.3 Установка зависимостей

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install psycopg2-binary
```

### 15.4 Применение миграций

```bash
export DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/time_manager
alembic upgrade head
```

### 15.5 Запуск API

```bash
uvicorn app.main:app --reload
```

После запуска открыть:

```text
http://127.0.0.1:8000/docs
```

## 16. Проверка через Swagger

FastAPI автоматически создает Swagger-документацию.

Адрес:

```text
http://127.0.0.1:8000/docs
```

Порядок проверки:

1. Выполнить `POST /auth/register`.
2. Выполнить `POST /auth/login`.
3. Скопировать JWT-токен.
4. Нажать `Authorize`.
5. Вставить токен в формате `Bearer <token>`.
6. Выполнить `GET /users/me`.
7. Проверить CRUD для `/projects`, `/tasks`, `/tags`.

## 17. Что показывать на защите

Минимальный план демонстрации:

1. Открыть Swagger `/docs`.
2. Показать регистрацию пользователя.
3. Показать вход и получение JWT.
4. Через `Authorize` вставить токен.
5. Выполнить `GET /users/me`.
6. Создать проект через `POST /projects`.
7. Получить список проектов через `GET /projects`.
8. Открыть код:
   - `app/main.py`
   - `app/models.py`
   - `app/auth.py`
   - `app/database.py`
   - `alembic/`

## 18. Краткий вывод

В лабораторной работе реализовано серверное приложение на FastAPI для тайм-менеджмента. В проекте есть PostgreSQL, ORM SQLAlchemy, миграции Alembic, Pydantic-схемы, CRUD-операции, связи one-to-many и many-to-many, ручная JWT-аутентификация и хэширование паролей.
