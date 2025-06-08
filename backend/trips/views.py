from .models import Trip
from rest_framework.viewsets import ModelViewSet
from .serializers import TripSerializer
from users.permissions import IsClerkAuthenticated
# Create your views here.
class TripViewSet(ModelViewSet):
    serializer_class = TripSerializer
    permission_classes = [IsClerkAuthenticated]
    lookup_field = 'slug' 

    def get_queryset(self):
        return Trip.objects.filter(user_profile=self.request.user_profile).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user_profile)
    
    
