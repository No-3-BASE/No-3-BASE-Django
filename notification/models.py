from django.db import models
from django.conf import settings
from article.models import Comment

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='notification')
    link = models.URLField(blank=True, null=True)
    isRead = models.BooleanField(default=False)
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient} - {self.title}"
