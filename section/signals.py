from django.db.models.signals import post_save
from django.dispatch import receiver
from board.models import Section
from .models import Category

@receiver(post_save, sender=Section)
def create_default_category(sender, instance, created, **kwargs):
    if created:
        Category.objects.create(
            section=instance,
            name="默認類別"
        )