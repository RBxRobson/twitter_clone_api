from django.db import models
from .user import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=255, default='')
    avatar = models.ImageField(upload_to='placeholders/', default='avatar_placeholder.png')
    header = models.ImageField(upload_to='placeholders/', default='header_placeholder.png')

    def __str__(self):
        return f'Profile of {self.user.username}'