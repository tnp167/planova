from django.db import models
from users.models import UserProfile  

TRIP_TYPE_CHOICES = [
    ('solo', 'Solo'),
    ('couple', 'Couple'),
    ('family', 'Family'),
    ('friends', 'Friends'),
]

class Trip(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="trips")
    name = models.CharField(max_length=255)
    location_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10, blank=False, null=False)
    mapbox_id = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    trip_type = models.CharField(max_length=10, choices=TRIP_TYPE_CHOICES, default='solo')
    num_adults = models.PositiveSmallIntegerField()
    num_children = models.PositiveSmallIntegerField(default=0)
    num_infants = models.PositiveSmallIntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"
