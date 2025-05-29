from django.urls import path
from .views import autocomplete_location, autocomplete_hotels, autocomplete_addresses

urlpatterns = [
    path('autocomplete/', autocomplete_location, name='autocomplete_location'),
    path('hotel-autocomplete/', autocomplete_hotels, name='autocomplete_hotels'),
    path('address-autocomplete/', autocomplete_addresses, name='autocomplete_addresses'),
]
