from django import template
from ..models import Follow

register = template.Library()

@register.filter
def is_following(user, target_user):
    return Follow.objects.filter(follower=user, following=target_user).exists()