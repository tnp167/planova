from django.shortcuts import render
from django.http import JsonResponse
from .models import Trip
from users.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging


# Create your views here.
@csrf_exempt
@require_http_methods(["GET"])
def get_trips(request):
    try:
        user_profile = request.user_profile
        trips = Trip.objects.filter(user_profile=user_profile).order_by('-created_at').values()
        return JsonResponse(list(trips), safe=False)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

