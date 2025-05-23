from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
#用戶
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username

#用戶資料
class Profile(models.Model):
    player = models.OneToOneField('player.CustomUser', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='player_photo', blank=True, null=True)
    exp = models.IntegerField(default=0)

    def __str__(self):
        return self.player.username