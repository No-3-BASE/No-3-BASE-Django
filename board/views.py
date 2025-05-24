from django.shortcuts import render
from .models import Section
from datetime import datetime, timezone

def home_view(request):
    #全部板塊
    allSection = Section.objects.all()

    #熱度最高板塊
    hotSections = Section.objects.order_by(
        '-yesterday_hot', '-total_hot', '-created_at'
    )[:12]

    if request.user.is_authenticated:
        print("用戶處於登入狀態")
        profile = request.user.profile
        now = datetime.now(timezone.utc).date()

        if profile.loginExpGainDate != now:
            print("尚未獲得登入經驗")
            profile.exp += 5
            profile.loginExpGainDate = now
            profile.recalculate_level()
            profile.save()

    return render(request, 'board/index.html', {
        'hot_sections': hotSections,
        'all_sections': allSection
    })
