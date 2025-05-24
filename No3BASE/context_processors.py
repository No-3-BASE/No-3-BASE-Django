from player.models import Profile
from datetime import datetime, timezone
import math

def toolbar_context(request):
    print(f"目前登入狀態 {request.user.is_authenticated}")
    if request.user.is_authenticated:
        user = request.user
        now = datetime.now(timezone.utc)
        signupDays = (now - user.date_joined).days + 1

        level = 0
        totalExpNeeded = 0
        nextLevelExp = 70
        progress = 0.0
        expInLevel = 0
        expToNext = 0
        progress = 0

        profile = None

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = None


        if profile and profile.exp is not None:
            a = 70
            exp = profile.exp
            level = 0
            totalExpNeeded = 0
            nextLevelExp = 0

            while True:
                nextLevelExp = totalExpNeeded + a * (level + 1)
                if exp < nextLevelExp:
                    break
                totalExpNeeded = nextLevelExp
                level += 1
                if level > 999:
                    break

            expInLevel = exp - totalExpNeeded
            expToNext = a * (level + 1)
            progress = round((expInLevel / expToNext) * 100, 2) if expToNext > 0 else 100.0

            if progress > 100.0:
                progress = 100.0

            print(totalExpNeeded)
            print(nextLevelExp)
            print(level)
            
            if level > 999:
                level = 999
                expInLevel = "∞"
                expToNext = "MAX"
                progress = 100.0

        return {
            'toolBar': {
                'isLogin': True,
                'name': user.first_name,
                'signupDays': signupDays,
                'profile': profile,
                'level': level,
                'expInLevel': expInLevel,
                'expToNext': expToNext,
                'progressPercent': progress
            }
        }
    
    return {
        'toolBar': {
            'isLogin': False,
            'name': "訪客",
            'signupDays': 0,
            'profile': None,
            'level': 0,
            'currentLevelExp': 0,
            'nextLevelExp': 0,
            'progressPercent': 0
        }
    }