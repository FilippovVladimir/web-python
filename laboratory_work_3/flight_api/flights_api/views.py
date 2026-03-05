from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Flight, Reservation, Review
from .serializers import FlightSerializer, ReservationSerializer, ReviewSerializer
from .permissions import IsOwnerOrReadOnly

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().order_by("-departure_time")
    serializer_class = FlightSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["flight_number", "airline", "departure_city", "arrival_city", "gate"]
    ordering_fields = ["departure_time", "arrival_time", "flight_number"]

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["seat", "ticket_number", "flight__flight_number", "flight__airline"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).select_related("flight").order_by("-created_at")


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.select_related("flight", "author").order_by("-created_at")

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
