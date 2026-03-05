from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Flight(models.Model):
    FLIGHT_TYPE_CHOICES = [
        ("arrival", "Прилёт"),
        ("departure", "Вылет"),
    ]

    flight_number = models.CharField("Номер рейса", max_length=20)
    airline = models.CharField("Авиакомпания", max_length=100)
    departure_city = models.CharField("Город вылета", max_length=100)
    arrival_city = models.CharField("Город прилёта", max_length=100)

    departure_time = models.DateTimeField("Время вылета")
    arrival_time = models.DateTimeField("Время прилёта")
    flight_type = models.CharField("Тип рейса", max_length=10, choices=FLIGHT_TYPE_CHOICES)
    gate = models.CharField("Гейт", max_length=10)

    class Meta:
        verbose_name = "Рейс"
        verbose_name_plural = "Рейсы"

    def __str__(self):
        return f"{self.flight_number} — {self.airline}"


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="reservations", verbose_name="Рейс")
    seat = models.CharField("Место", max_length=10)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    ticket_number = models.CharField("Номер билета", max_length=50, blank=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        unique_together = ("flight", "user", "seat")

    def __str__(self):
        return f"{self.user} -> {self.flight} seat {self.seat}"


class Review(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="reviews", verbose_name="Рейс")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор")
    flight_date = models.DateField("Дата рейса")
    text = models.TextField("Текст отзыва")
    rating = models.IntegerField("Рейтинг (1-10)", validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв {self.flight} ({self.rating})"
