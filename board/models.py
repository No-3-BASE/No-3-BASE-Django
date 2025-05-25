from django.db import models
import uuid
#板塊
class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='section_icon', blank=True, null=True)
    background = models.ImageField(upload_to='section_background', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    slogan = models.CharField(max_length=160, blank=True, default='　')

    yesterdayPosts = models.IntegerField(default=0)
    yesterdayHot = models.IntegerField(default=0)

    totalPosts = models.IntegerField(default=0)
    totalHot = models.IntegerField(default=0)

    def __str__(self):
        return self.name