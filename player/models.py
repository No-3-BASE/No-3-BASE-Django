from django.contrib.auth.models import AbstractUser
from datetime import datetime, timezone
from django.db import models
from django.conf import settings
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

    @property
    def signupDays(self):
        if self.player and self.player.date_joined:
            now = datetime.now(timezone.utc)
            return (now - self.player.date_joined).days + 1
        return 0

    def __str__(self):
        return self.player.username

    #經驗計算
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
    
    #關注篩選
    def is_following(self, other_user):
        return Follow.objects.filter(follower=self, following=other_user).exists()

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers_set', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"