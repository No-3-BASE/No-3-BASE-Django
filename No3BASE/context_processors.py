from datetime import datetime, timezone
from player.models import Profile
from notification.models import Notification
from article.models import Article
import math

def toolbar_context(request):
    print(f"目前登入狀態 {request.user.is_authenticated}")
    if request.user.is_authenticated:
        user = request.user
        now = datetime.now(timezone.utc)

        notifies = None

        profile = None

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = None

        try:
            notifies = Notification.objects.filter(recipient=user)[:20]
        except Notification.DoesNotExist:
            notifies = None

        article_count = Article.objects.filter(author=user, status='published').count()

        return {
            'toolBar': {
                'isLogin': True,
                'notifies': notifies,
                'id': user.id,
                'name': user.first_name,
                'profile': profile,
                'article': article_count
            }
        }
    
    return {
        'toolBar': {
            'isLogin': False,
            'notify': None,
            'id': None,
            'name': "訪客",
            'profile': None,
            'article': None
        }
    }