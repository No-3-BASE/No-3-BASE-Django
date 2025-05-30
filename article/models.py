from django.db import models
from django.conf import settings
from django.utils.html import strip_tags
from board.models import Section
from section.models import Category
import uuid
import re
#文章
class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('deleted', '已刪除草稿'),
        ('pending', '待審核'),
        ('rejected', '已退回'),
        ('published', '已發布'),
        ('removed', '已刪除文章'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='articles')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles', on_delete=models.CASCADE, related_query_name='articles')
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='articles')
    title = models.TextField(null=True)
    content = models.TextField(null=True)
    createAt = models.DateTimeField(auto_now_add=True)
    lastEdit = models.DateTimeField(auto_now=True)
    publishAt = models.DateTimeField(null=True, blank=True)

    like = models.IntegerField(default=0)
    comment = models.IntegerField(default=0)
    hot = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.get_status_display()} - {self.section.name if self.section else 'No Section'} - {self.category.name if self.category else 'No Category'} - {self.title}"
    
    #純文字提取
    def get_preview(self, length=200):
        content = self.content or ''
        content = re.sub(r'</p\s*>', '\n', content, flags=re.IGNORECASE)
        text = strip_tags(content)
        text = text.strip()
        
        if len(text) > length:
            return text[:length]
        return text
    
#留言
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='comments', on_delete=models.SET_NULL)
    content = models.TextField()
    floor = models.PositiveIntegerField(default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    like = models.PositiveIntegerField(default=0)

    parentComment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.article.title} - {self.content}"
    
    def save(self, *args, **kwargs):
        if not self.floor:
            last_floor = Comment.objects.filter(article=self.article).aggregate(
                max_floor=models.Max('floor')
            )['max_floor'] or 0
            self.floor = last_floor + 1
        super().save(*args, **kwargs)