from django.db import models
from users.models import UserProfile  
from django.utils.text import slugify
import uuid

TRIP_TYPE_CHOICES = [
    ('solo', 'Solo'),
    ('couple', 'Couple'),
    ('family', 'Family'),
    ('friends', 'Friends'),
]


TRIP_STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]


class Trip(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="trips")
    name = models.CharField(max_length=255)
    location_name = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    mapbox_id = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    trip_type = models.CharField(max_length=10, choices=TRIP_TYPE_CHOICES, default='solo')
    num_adults = models.PositiveSmallIntegerField(default=1)
    num_children = models.PositiveSmallIntegerField(default=0)
    num_infants = models.PositiveSmallIntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=TRIP_STATUS_CHOICES, default='draft')

    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name or "trip").lower()
            unique_suffix = uuid.uuid4().hex[:6]
            self.slug = f"{base_slug}-{unique_suffix}"
        super().save(*args, **kwargs)
    
