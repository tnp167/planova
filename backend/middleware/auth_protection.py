import os
from django.http import JsonResponse
from clerk_backend_api import Clerk
from clerk_backend_api.jwks_helpers import authenticate_request, AuthenticateRequestOptions
from users.models import UserProfile
import httpx

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

PROTECTED_PATHS = ["/api/location/", "/api/trips/"]

env = os.getenv("DJANGO_ENV", "development")

class ClerkAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.clerk = Clerk(bearer_auth=CLERK_SECRET_KEY)

    def __call__(self, request):
        if not any(request.path.startswith(path) for path in PROTECTED_PATHS):
            return self.get_response(request)

        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Missing auth header"}, status=401)

        try:
            httpx_request = httpx.Request(
                method=request.method,
                url=request.build_absolute_uri(),
                headers={"Authorization": token}
            )
            
            if os.getenv("DJANGO_ENV") == "production":
                options = AuthenticateRequestOptions(authorized_parties=["https://planova.travel"])
            else:
                options = AuthenticateRequestOptions()
            result = self.clerk.authenticate_request(httpx_request, options)

            if not result.is_signed_in:
                return JsonResponse({"error": "Unauthorized"}, status=401)

            request.clerk_user = result.payload

            # Get the user profile
            clerk_user_id = result.payload.get("sub")
            try:
                request.user_profile = UserProfile.objects.get(clerk_user_id=clerk_user_id)
            except UserProfile.DoesNotExist:
                return JsonResponse({"error": "User profile not found"}, status=403)

        except Exception as e:
            print("Clerk Auth Exception:", e)
            return JsonResponse({"error": "Unauthorized"}, status=401)

        return self.get_response(request)
