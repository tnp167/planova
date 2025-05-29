from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from amadeus import Client, Hotel
import requests
# Create your views here.

amadeus = Client(
    client_id=settings.AMADEUS_CLIENT_ID,
    client_secret=settings.AMADEUS_CLIENT_SECRET,
)

class Hotel:
    HOTEL_GDS = "HOTEL_GDS"
    HOTEL_LEISURE = "HOTEL_LEISURE"

@csrf_exempt
def autocomplete_location(request):
    query = request.GET.get('q')
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)
    
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json"
    params = {
        'access_token': settings.MAPBOX_ACCESS_TOKEN,
        'limit': 5
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def autocomplete_hotels(request):
    query = request.GET.get('q', '')
    country_code = request.GET.get('countryCode', '')  

    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)
    try:
        response = amadeus.reference_data.locations.hotel.get(keyword=query, subType=[Hotel.HOTEL_GDS, Hotel.HOTEL_LEISURE], countryCode=country_code)
        return JsonResponse(response.data, status=200, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def autocomplete_addresses(request):
    query = request.GET.get('q', '')
    country_code = request.GET.get('countryCode', '')  

    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)
    
    url = f"https://api.mapbox.com/search/geocode/v6/forward"
    params = {
        'q': query,
        'country': country_code,
        'access_token': settings.MAPBOX_ACCESS_TOKEN
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
