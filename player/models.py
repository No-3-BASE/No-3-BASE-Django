from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField('player.CustomUser', on_delete=models.CASCADE)
    exp = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username