from django.db import models
from board.models import Section
import uuid
#類別區塊
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('section', 'name')

    def __str__(self):
        return f"{self.section.name} - {self.name}"
