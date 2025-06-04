from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from amadeus import Client, Hotel
import requests
from django.core.cache import caches
from django.views.decorators.http import require_http_methods
from io import BytesIO
from urllib.parse import quote_plus
import boto3 

# Create your views here.

amadeus = Client(
    client_id=settings.AMADEUS_CLIENT_ID,
    client_secret=settings.AMADEUS_CLIENT_SECRET,
)

s3 = boto3.client('s3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

class Hotel:
    HOTEL_GDS = "HOTEL_GDS"
    HOTEL_LEISURE = "HOTEL_LEISURE"

@csrf_exempt
@require_http_methods(["GET"])
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
@require_http_methods(["GET"])
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
@require_http_methods(["GET"])
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
    

@csrf_exempt
@require_http_methods(["GET"])
def get_city_image(request):
    query = request.GET.get('q', '').strip().lower()
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)
    
    safe_query = quote_plus(query)
    cache_key = f"city_image_{safe_query}"
    cached_image = caches['default'].get(cache_key)

    if cached_image:
        return JsonResponse({"imageUrl": cached_image}, status=200)
    
    try:
        response = requests.get("https://api.unsplash.com/search/photos", params={
            'query': query,
            "per_page": 1,
            "orientation": "landscape",
        }, headers={
            "Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}"
        })
        response.raise_for_status()
        data = response.json()
        image_url = data["results"][0]["urls"]["raw"] if data["results"] else None
        image_url += "&w=400&h=200&fit=crop"

        # Download the image and save it to S3
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        image_data = BytesIO(image_response.content)

        s3_filename = f"city_images/{query}.jpg"
        try:
            s3.upload_fileobj(image_data, settings.AWS_S3_BUCKET_NAME, s3_filename)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        s3_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_filename}"

        caches['default'].set(cache_key, s3_url, timeout=60 * 60 * 24 * 7)

        return JsonResponse({"imageUrl": s3_url}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
