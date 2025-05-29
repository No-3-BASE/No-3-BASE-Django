from django.db import models
from django.conf import settings
from board.models import Section
from section.models import Category
import uuid
#草稿
class Draft(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='drafts', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.SET_NULL, related_name='drafts')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='drafts')
    title = models.CharField(null=True)
    content = models.CharField(null=True)
    createAt = models.DateField(auto_now_add=True)
    lastEdit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[草稿] {self.section.name} - {self.category.name} - {self.title or '暫無標題'}"

#文章
class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='articles')
    title = models.CharField(null=False)
    content = models.CharField(null=True)
    createAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.section.name} - {self.category.name} - {self.title}"