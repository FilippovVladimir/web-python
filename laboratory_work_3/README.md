# Лабораторная работа №3 — Django REST Framework + Djoser (рейсы)

## Установка и запуск (SQLite)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd flight_api
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Открыть:
- http://127.0.0.1:8000/api/  (Browsable API)
- http://127.0.0.1:8000/admin/ (админка)

## Авторизация по токену (Djoser)
Регистрация:
- POST /api/auth/users/
  JSON: {"username":"user1","password":"12345678","re_password":"12345678"}

Получить токен:
- POST /api/auth/token/login/
  JSON: {"username":"user1","password":"12345678"}

Ответ: {"auth_token":"..."} — этот токен использовать в запросах:
Header: Authorization: Token <token>

Текущий пользователь:
- GET /api/auth/users/me/

Выход (удалить токен):
- POST /api/auth/token/logout/

## Эндпоинты
- /api/flights/
  - GET доступен всем
  - POST/PUT/PATCH/DELETE только админ

- /api/reservations/
  - доступ только авторизованным
  - пользователь видит и меняет только свои бронирования

- /api/reviews/
  - GET доступен всем
  - создание/редактирование/удаление — только авторизованный и только свои


## Seed (тестовые данные)
```bash
python manage.py seed
```

## Запуск после закрытия терминала
```bash
cd flight_api
source ../.venv/bin/activate
python manage.py runserver
```
