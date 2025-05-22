from django.db import models
import uuid
#板塊
class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='section_icon', blank=True, null=True)
    background = models.ImageField(upload_to='section_background', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slogan = models.CharField(max_length=160, blank=True, default='　')

    yesterday_posts = models.IntegerField(default=0)
    yesterday_hot = models.IntegerField(default=0)

    total_posts = models.IntegerField(default=0)
    total_hot = models.IntegerField(default=0)

    def __str__(self):
        return self.name