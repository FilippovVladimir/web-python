# Лабораторная работа №4 — Vue.js клиент к API рейсов (ЛР3)

## Что реализовано (простая версия)
- Vue 3 + Vite
- Bootstrap 5 (как UI-библиотека, аналог Vuetify)
- Регистрация / Вход / Выход (Djoser + токены)
- Список рейсов + поиск (GET /api/flights/?search=...)
- Создание бронирования (POST /api/reservations/)
- Просмотр/удаление своих бронирований (GET/DELETE /api/reservations/)
- Просмотр и добавление отзывов (GET/POST /api/reviews/)
- Страница аккаунта (GET/PATCH /api/auth/users/me/)

## Запуск фронтенда
Нужен Node.js (LTS).

```bash
cd flight-frontend
npm install
cp .env.example .env
npm run dev
```

Открыть: http://localhost:5173

## Запуск backend (ЛР3)
В отдельном терминале:
```bash
cd flight_api
source ../.venv/bin/activate
python manage.py runserver
```

## CORS (чтобы Vue мог обращаться к Django)
На backend (ЛР3):

1) Установить:
```bash
pip install django-cors-headers
```

2) `flight_api/settings.py`:
- в `INSTALLED_APPS` добавить:
```python
'corsheaders',
```
- в `MIDDLEWARE` добавить (сверху):
```python
'corsheaders.middleware.CorsMiddleware',
```
- добавить:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

Перезапустить backend.

## Проверка
1) Открыть “Рейсы” — список должен загрузиться
2) Регистрация/вход
3) “Забронировать” рейс → “Мои брони”
4) Добавить отзыв → “Отзывы”
