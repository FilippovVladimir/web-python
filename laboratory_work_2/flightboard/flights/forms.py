from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Review

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ("seat",)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("flight_date", "text", "rating")
        widgets = {
            "flight_date": forms.DateInput(attrs={"type": "date"}),
        }
