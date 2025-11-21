# myapp/models.py

from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/profile/{filename}'

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=user_directory_path, 
        blank=True, 
        null=True
    )

    def __str__(self):
        return f'Perfil de {self.user.username}'