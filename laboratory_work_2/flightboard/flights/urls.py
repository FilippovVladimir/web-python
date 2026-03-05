from django.urls import path
from . import views

app_name = "flights"

urlpatterns = [
    path("", views.flight_list, name="flight_list"),
    path("register/", views.register, name="register"),
    path("flight/<int:pk>/", views.flight_detail, name="flight_detail"),

    path("flight/<int:pk>/reserve/", views.reserve_create, name="reserve_create"),
    path("my-reservations/", views.my_reservations, name="my_reservations"),
    path("reservation/<int:pk>/edit/", views.reserve_edit, name="reserve_edit"),
    path("reservation/<int:pk>/delete/", views.reserve_delete, name="reserve_delete"),

    path("flight/<int:pk>/review/", views.review_create, name="review_create"),
]
