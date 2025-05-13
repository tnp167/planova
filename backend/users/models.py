from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    clerk_user_id = models.CharField(max_length=255, unique=True)
    picture = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.email 
