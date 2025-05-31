from datetime import datetime, timezone
from player.models import Profile
from article.models import Article
import math

def toolbar_context(request):
    print(f"目前登入狀態 {request.user.is_authenticated}")
    if request.user.is_authenticated:
        user = request.user
        now = datetime.now(timezone.utc)
        signupDays = (now - user.date_joined).days + 1

        profile = None

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = None

        article_count = Article.objects.filter(author=user, status='published').count()

        return {
            'toolBar': {
                'isLogin': True,
                'id': user.id,
                'name': user.first_name,
                'profile': profile,
                'article': article_count
            }
        }
    
    return {
        'toolBar': {
            'isLogin': False,
            'id': None,
            'name': "訪客",
            'profile': None,
            'article': None
        }
    }