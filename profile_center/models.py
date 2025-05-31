from django.db import models
from django.conf import settings
from board.models import Section
import uuid

class GameCard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.SET_NULL)
    customName = models.CharField(max_length=255, blank=True)
    uid = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('player', 'section', 'uid')

    def __str__(self):
        return f"{self.customName} - {self.uid}" or f"{self.section.name} - {self.uid}"
