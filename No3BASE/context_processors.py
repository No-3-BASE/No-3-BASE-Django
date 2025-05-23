from player.models import Profile
from datetime import datetime, timezone

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

        return {
            'toolBar': {
                'isLogin': True,
                'name': user.first_name,
                'signupDays': signupDays,
                'profile': profile
            }
        }
    
    return {
        'toolBar': {
            'isLogin': False,
            'name': "訪客",
            'signupDays': 0,
            'profile': None,
        }
    }