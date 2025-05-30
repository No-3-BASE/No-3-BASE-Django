from django.db import models
import uuid
#板塊
class Section(models.Model):
    PLATFORM_CHOICES = [
        ('PC', '電腦遊戲'),
        ('Console', '家用主機遊戲'),
        ('Mobile', '手機遊戲'),
        ('Browser', '網頁遊戲'),
        ('Cloud', '雲端遊戲'),
        ('Arcade', '街機遊戲'),
        ('Handheld', '掌機遊戲'),
        ('VR', '虛擬實境遊戲'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='section_icon', blank=True, null=True)
    background = models.ImageField(upload_to='section_background', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    slogan = models.CharField(max_length=160, blank=True, default='　')
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES, default='PC')

    yesterdayPosts = models.IntegerField(default=0)
    yesterdayHot = models.IntegerField(default=0)

    totalPosts = models.IntegerField(default=0)
    totalHot = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.get_platform_display()} - {self.name}"