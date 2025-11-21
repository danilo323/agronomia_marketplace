# myapp/models.py

from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/profile/{filename}'

class Profile(models.Model):
    AUTH_PROVIDERS = [
        ('email', 'Email/Password'),
        ('google', 'Google'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=user_directory_path, 
        blank=True, 
        null=True
    )
    auth_provider = models.CharField(
        max_length=20,
        choices=AUTH_PROVIDERS,
        default='email',
        help_text='Método de autenticación usado por el usuario'
    )

    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    def can_change_password(self):
        """Retorna True si el usuario puede cambiar contraseña (no usa Google OAuth)"""
        return self.auth_provider == 'email'