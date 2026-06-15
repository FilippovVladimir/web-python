# Лабораторная работа 2 (II семестр)

## Цель
Изучить отличия threading, multiprocessing и asyncio в Python.

## Задача 1. Сумма чисел от 1 до 10 000 000 000 000

Три программы делят диапазон на 8 частей и считают сумму параллельно.

| Файл | Подход |
|---|---|
| `task1/threading_sum.py` | `threading` |
| `task1/multiprocessing_sum.py` | `multiprocessing` |
| `task1/async_sum.py` | `asyncio` |

### Результаты

| Подход | Сумма | Время |
|---|---|---|
| threading | 50000000000005000000000000 | 0.0030 сек |
| multiprocessing | 50000000000005000000000000 | 0.1697 сек |
| async | 50000000000005000000000000 | 0.0064 сек |

### Вывод

Все программы дали одинаковый результат. Разница во времени связана с накладными расходами: multiprocessing дольше из-за запуска процессов, threading и async быстрее на короткой задаче. Для CPU-нагрузки лучше multiprocessing, для I/O — async или threading.

## Задача 2. Параллельный парсинг веб-страниц

Три программы парсят заголовки страниц и сохраняют их в PostgreSQL (`time_manager`, таблица `parsed_pages`).

| Файл | Подход |
|---|---|
| `task2/threading_parser.py` | `threading` + `requests` |
| `task2/multiprocessing_parser.py` | `multiprocessing` + `requests` |
| `task2/async_parser.py` | `asyncio` + `aiohttp` |

URL-адреса делятся на 4 части для параллельной обработки.

### Результаты

| Подход | Время |
|---|---|
| threading | 0.7157 сек |
| multiprocessing | 0.8921 сек |
| async | 0.5813 сек |

### Вывод

Async оказался быстрее, потому что запросы к сайтам выполняются без блокировки. Threading тоже эффективен для I/O. Multiprocessing медленнее из-за запуска отдельных процессов.

## Запуск

```bash
cd laboratory_work_6
pip install -r requirements.txt
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/time_manager"

cd task1
python threading_sum.py
python multiprocessing_sum.py
python async_sum.py

cd ../task2
python threading_parser.py
python multiprocessing_parser.py
python async_parser.py
```

## Общий вывод

Threading и async подходят для сетевых задач. Multiprocessing — для тяжёлых вычислений на CPU.
