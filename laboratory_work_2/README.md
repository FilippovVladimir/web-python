# Лабораторная работа №2 — Django (вариант 3: табло авиаперелётов)

## Функционал (по заданию)
- Регистрация новых пользователей
- Просмотр рейсов
- Резервирование мест на рейсах (создание/редактирование/удаление своих бронирований)
- Администратор может вписать номер билета для брони в Django-admin
- Таблица пассажиров рейса (на странице рейса)
- Отзывы к рейсам (дата рейса, текст, рейтинг 1-10, автор)
- Bootstrap меню + пагинация + поиск

## Быстрый запуск (SQLite)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd flightboard
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Открыть: http://127.0.0.1:8000  
Админка: http://127.0.0.1:8000/admin
