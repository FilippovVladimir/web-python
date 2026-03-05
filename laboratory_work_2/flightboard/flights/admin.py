from django.contrib import admin
from .models import Flight, Reservation, Review

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("flight_number", "airline", "departure_city", "arrival_city", "departure_time", "arrival_time", "flight_type", "gate")
    search_fields = ("flight_number", "airline", "departure_city", "arrival_city", "gate")
    list_filter = ("flight_type", "airline")

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("flight", "user", "seat", "ticket_number", "created_at")
    search_fields = ("ticket_number", "seat", "user__username", "flight__flight_number")
    list_filter = ("flight",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("flight", "author", "flight_date", "rating", "created_at")
    search_fields = ("flight__flight_number", "author__username", "text")
    list_filter = ("rating", "flight_date")
