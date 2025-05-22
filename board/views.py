from django.shortcuts import render
from .models import Section

def home_view(request):
    #全部板塊
    allSection = Section.objects.all()

    #熱度最高板塊
    hotSections = Section.objects.order_by(
        '-yesterday_hot', '-total_hot', '-created_at'
    )[:12]

    return render(request, 'board/index.html', {
        'hot_sections': hotSections,
        'all_sections': allSection
    })
