from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from flights_api import views

router = SimpleRouter()
router.register(r"flights", views.FlightViewSet, basename="flights")
router.register(r"reservations", views.ReservationViewSet, basename="reservations")
router.register(r"reviews", views.ReviewViewSet, basename="reviews")

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include(router.urls)),

    # Вход через браузер для browsable API
    path("api-auth/", include("rest_framework.urls")),

    # Djoser
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
]