from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from datetime import datetime, timezone

User = get_user_model()

class ActivityTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        user = request.user
        profile = None
        today = now().date()

        try:
            profile = user.profile
            current = datetime.now(timezone.utc).date()

            if profile.loginExpGainDate != current:
                profile.exp += 5
                profile.loginExpGainDate = current
                profile.recalculate_level()
                profile.save()

        except User.DoesNotExist:
            pass

        if not hasattr(profile, '_lastSeen_updated'):
            
            profile.lastSeen = now()
            profile.save(update_fields=['lastSeen'])
            profile._lasSeen_updated = True
