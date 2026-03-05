from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, ReservationForm, ReviewForm
from .models import Flight, Reservation, Review

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("flights:flight_list")
    else:
        form = RegisterForm()
    return render(request, "flights/register.html", {"form": form})

def flight_list(request):
    q = request.GET.get("q", "").strip()

    flights = Flight.objects.all().order_by("-departure_time")
    if q:
        flights = flights.filter(
            Q(flight_number__icontains=q)
            | Q(airline__icontains=q)
            | Q(departure_city__icontains=q)
            | Q(arrival_city__icontains=q)
            | Q(gate__icontains=q)
        )

    paginator = Paginator(flights, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "flights/flight_list.html", {"page_obj": page_obj, "q": q})

def flight_detail(request, pk: int):
    flight = get_object_or_404(Flight, pk=pk)
    passengers = Reservation.objects.filter(flight=flight).select_related("user").order_by("seat")
    reviews = Review.objects.filter(flight=flight).select_related("author").order_by("-created_at")
    return render(request, "flights/flight_detail.html", {"flight": flight, "passengers": passengers, "reviews": reviews})

@login_required
def reserve_create(request, pk: int):
    flight = get_object_or_404(Flight, pk=pk)

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            seat = form.cleaned_data["seat"].strip()
            Reservation.objects.create(flight=flight, user=request.user, seat=seat)
            messages.success(request, "Бронирование создано.")
            return redirect("flights:my_reservations")
    else:
        form = ReservationForm()

    return render(request, "flights/reservation_form.html", {"form": form, "flight": flight, "title": "Забронировать место"})

@login_required
def my_reservations(request):
    q = request.GET.get("q", "").strip()

    reservations = Reservation.objects.filter(user=request.user).select_related("flight").order_by("-created_at")
    if q:
        reservations = reservations.filter(
            Q(flight__flight_number__icontains=q)
            | Q(flight__airline__icontains=q)
            | Q(seat__icontains=q)
            | Q(ticket_number__icontains=q)
        )

    paginator = Paginator(reservations, 7)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "flights/my_reservations.html", {"page_obj": page_obj, "q": q})

@login_required
def reserve_edit(request, pk: int):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, "Бронирование изменено.")
            return redirect("flights:my_reservations")
    else:
        form = ReservationForm(instance=reservation)

    return render(request, "flights/reservation_form.html", {"form": form, "flight": reservation.flight, "title": "Изменить бронирование"})

@login_required
def reserve_delete(request, pk: int):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)

    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Бронирование удалено.")
        return redirect("flights:my_reservations")

    return render(request, "flights/reservation_delete.html", {"reservation": reservation})

@login_required
def review_create(request, pk: int):
    flight = get_object_or_404(Flight, pk=pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.flight = flight
            review.author = request.user
            review.save()
            messages.success(request, "Отзыв добавлен.")
            return redirect("flights:flight_detail", pk=flight.pk)
    else:
        form = ReviewForm()

    return render(request, "flights/review_form.html", {"form": form, "flight": flight})
