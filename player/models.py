from django.contrib.auth.models import AbstractUser
from datetime import datetime, timezone, date, timedelta
from django.utils import timezone as tz
from django.db import models
from django.conf import settings
from datetime import date
from article.models import Comment
import uuid
import os

#照片上傳
def user_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.player.id}.{ext}'
    return os.path.join('player_photo', filename)

#用戶
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username

#用戶資料
class Profile(models.Model):
    player = models.OneToOneField('player.CustomUser', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_photo_path, blank=True, null=True)
    backgroundPhoto = models.ImageField(upload_to=user_photo_path, blank=True, null=True)
    slogan = models.CharField(max_length=200, blank=True, default='在基地深處，訊號永不熄滅，識別者並未在此留下痕跡')
    birthday = models.DateField(default=date(2000, 1, 1), blank=True, null=True)

    lastSeen = models.DateTimeField(default=tz.now)

    loginExpGainDate = models.DateField(blank=True, null=True)
    draftExpGainDate = models.DateField(blank=True, null=True)
    articleExpGainDate = models.DateField(blank=True, null=True)
    messageExpGainDate = models.DateField(blank=True, null=True)
    likeExpGainDate = models.DateField(blank=True, null=True)

    exp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    expInLevel = models.IntegerField(default=0)
    expToNext = models.IntegerField(default=70)
    progressPercent = models.FloatField(default=0.0)

    #登入天數
    @property
    def signupDays(self):
        if self.player and self.player.date_joined:
            now = datetime.now(timezone.utc)
            return (now - self.player.date_joined).days + 1
        return 0
    
    #粉絲數
    @property
    def followerCount(self):
        return Follow.objects.filter(following=self.player).count()
    
    #關注數
    @property
    def followingCount(self):
        return Follow.objects.filter(follower=self.player).count()

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
    
    #單一任務判定
    def has_done_today(self, field_name):
        date = getattr(self, field_name)
        if not date:
            return False
        today = datetime.now(timezone.utc).date()
        return date == today
    
    #任務字典
    def get_daily_tasks_status(self):
        today = date.today()
        print(today)
        return {
            'loginDone': self.loginExpGainDate == today,
            'articleDone': self.articleExpGainDate == today,
            'messageDone': self.messageExpGainDate == today,
            'likeDone': self.likeExpGainDate == today,
            'draftDone': self.draftExpGainDate == today,
        }

class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers_set', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"