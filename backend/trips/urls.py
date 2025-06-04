from django.urls import path
from .views import get_trips

urlpatterns = [
    path("", get_trips, name="get_trips"),
]
