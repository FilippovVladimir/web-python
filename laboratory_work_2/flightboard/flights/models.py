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
    departure_city = models.CharField("Откуда", max_length=100)
    arrival_city = models.CharField("Куда", max_length=100)
    departure_time = models.DateTimeField("Вылет (время)")
    arrival_time = models.DateTimeField("Прилёт (время)")
    flight_type = models.CharField("Тип", max_length=10, choices=FLIGHT_TYPE_CHOICES)
    gate = models.CharField("Гейт", max_length=10)

    def __str__(self):
        return f"{self.flight_number} — {self.airline}"

class Reservation(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="reservations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    seat = models.CharField("Место", max_length=10)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    # Админ может вписать номер билета в админке
    ticket_number = models.CharField("Номер билета", max_length=50, blank=True)

    class Meta:
        unique_together = ("flight", "user", "seat")

    def __str__(self):
        return f"{self.user} -> {self.flight} seat {self.seat}"

class Review(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    flight_date = models.DateField("Дата рейса")
    text = models.TextField("Текст")
    rating = models.IntegerField("Рейтинг (1-10)", validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return f"Review {self.flight} by {self.author} ({self.rating})"
