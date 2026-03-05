from rest_framework import serializers
from .models import Flight, Reservation, Review

class FlightSerializer(serializers.ModelSerializer):
    flight_number = serializers.CharField(label="Номер рейса")
    airline = serializers.CharField(label="Авиакомпания")
    departure_city = serializers.CharField(label="Город вылета")
    arrival_city = serializers.CharField(label="Город прилёта")
    departure_time = serializers.DateTimeField(label="Время вылета")
    arrival_time = serializers.DateTimeField(label="Время прилёта")
    flight_type = serializers.ChoiceField(choices=Flight.FLIGHT_TYPE_CHOICES, label="Тип рейса")
    gate = serializers.CharField(label="Гейт")

    class Meta:
        model = Flight
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, label="Пользователь")

    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = ("created_at", "ticket_number")

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, label="Автор")

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("created_at",)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)
