import random
from datetime import timedelta, date

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from flights_api.models import Flight, Reservation, Review


class Command(BaseCommand):
    help = "Создаёт тестовые данные: 20 рейсов, 10 бронирований, 10 отзывов."

    def handle(self, *args, **options):
        User = get_user_model()

        # 1) Пользователи (обычные)
        user1, _ = User.objects.get_or_create(username="user1")
        if not user1.has_usable_password():
            user1.set_password("12345678")
            user1.save()

        user2, _ = User.objects.get_or_create(username="user2")
        if not user2.has_usable_password():
            user2.set_password("12345678")
            user2.save()

        # 2) Рейсы
        airlines = ["Аэрофлот", "S7 Airlines", "Победа", "Utair", "Ural Airlines", "Turkish Airlines", "Lufthansa", "Air France"]
        cities = ["Москва", "Санкт‑Петербург", "Казань", "Сочи", "Екатеринбург", "Новосибирск", "Минск", "Стамбул", "Берлин", "Париж"]

        created_flights = 0
        now = timezone.now()

        # Чтобы не плодить бесконечно, если команда запускается повторно:
        # если рейсов уже >= 20, просто не добавляем новые.
        existing = Flight.objects.count()
        target = 20
        need = max(0, target - existing)

        for i in range(need):
            dep = random.choice(cities)
            arr = random.choice([c for c in cities if c != dep])
            airline = random.choice(airlines)
            fnum = f"SU{random.randint(100, 999)}"
            dep_time = now + timedelta(hours=random.randint(1, 240))
            arr_time = dep_time + timedelta(hours=random.randint(1, 6))
            ftype = random.choice(["arrival", "departure"])
            gate = f"{random.choice(list('ABCD'))}{random.randint(1, 20)}"

            Flight.objects.create(
                flight_number=fnum,
                airline=airline,
                departure_city=dep,
                arrival_city=arr,
                departure_time=dep_time,
                arrival_time=arr_time,
                flight_type=ftype,
                gate=gate,
            )
            created_flights += 1

        self.stdout.write(self.style.SUCCESS(f"Рейсы: добавлено {created_flights}, всего {Flight.objects.count()}"))

        flights = list(Flight.objects.all().order_by("-departure_time")[:20])
        if not flights:
            self.stdout.write(self.style.WARNING("Нет рейсов — бронирования и отзывы не созданы."))
            return

        # 3) Бронирования (10)
        # Учитываем unique_together (flight, user, seat) — делаем разные места.
        users = [user1, user2]
        seats = [f"{random.choice(list('ABCDEF'))}{n}" for n in range(1, 51)]

        created_res = 0
        for _ in range(10):
            flight = random.choice(flights)
            user = random.choice(users)
            seat = random.choice(seats)

            if Reservation.objects.filter(flight=flight, user=user, seat=seat).exists():
                continue

            Reservation.objects.create(
                flight=flight,
                user=user,
                seat=seat,
                ticket_number=f"TK{random.randint(100000, 999999)}",
            )
            created_res += 1

        self.stdout.write(self.style.SUCCESS(f"Бронирования: добавлено {created_res}, всего {Reservation.objects.count()}"))

        # 4) Отзывы (10)
        created_rev = 0
        texts = [
            "Отличный перелёт, всё по расписанию.",
            "Небольшая задержка, но в целом нормально.",
            "Комфортно, экипаж вежливый.",
            "Не понравилась посадка, но долетели хорошо.",
            "Всё быстро и удобно, рекомендую.",
        ]

        for _ in range(10):
            flight = random.choice(flights)
            author = random.choice(users)

            Review.objects.create(
                flight=flight,
                author=author,
                flight_date=date.today(),
                text=random.choice(texts),
                rating=random.randint(6, 10),
            )
            created_rev += 1

        self.stdout.write(self.style.SUCCESS(f"Отзывы: добавлено {created_rev}, всего {Review.objects.count()}"))
        self.stdout.write(self.style.SUCCESS("Готово. Логин/пароль тестовых пользователей: user1/12345678, user2/12345678"))
