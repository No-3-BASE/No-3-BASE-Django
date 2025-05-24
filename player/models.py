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

    loginExpGainDate = models.DateField(blank=True, null=True)

    exp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    expInLevel = models.IntegerField(default=0)
    expToNext = models.IntegerField(default=70)
    progressPercent = models.FloatField(default=0.0)

    def __str__(self):
        return self.player.username

    def recalculate_level(self):
        a = 70
        exp = self.exp or 0
        level = 0
        totalExpNeeded = 0
        nextLevelExp = 0

        while True:
            nextLevelExp = totalExpNeeded + a * (level + 1)
            if exp < nextLevelExp:
                break
            totalExpNeeded = nextLevelExp
            level += 1
            if level > 999:
                break

        expInLevel = exp - totalExpNeeded
        expToNext = a * (level + 1)
        progress = round((expInLevel / expToNext) * 100, 2) if expToNext > 0 else 100.0

        if progress > 100.0:
            progress = 100.0

        if level > 999:
            level = 999
            expInLevel = -1
            expToNext = -1
            progress = 100.0

        self.level = level
        self.expInLevel = expInLevel
        self.expToNext = expToNext
        self.progressPercent = progress