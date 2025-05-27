from django.db import models
from board.models import Section

#類別區塊
class Category(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('section', 'name')

    def __str__(self):
        return f"{self.section.name} - {self.name}"
