from django.shortcuts import render
from player.models import Profile
from django.contrib.auth.decorators import login_required

@login_required
def player_profile_view(request):
    user = request.user

    try:
        profile = Profile.objects.get(player=user)
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'profile_center/player_profile.html', {
        'name': user.first_name,
        'profile': profile
    })

def edit_profile_view(request):
    return render(request, 'profile_center/edit_profile.html')

def edit_game_view(request):
    return render(request, 'profile_center/edit_game.html')

def daily_mission_view(request):
    return render(request, 'profile_center/daily_mission.html')

def my_article_view(request):
    return render(request, 'profile_center/my_article.html')

def my_draft_view(request):
    return render(request, 'profile_center/my_draft.html')

def my_bookmark_view(request):
    return render(request, 'profile_center/my_bookmark.html')

def my_fans_view(request):
    return render(request, 'profile_center/my_fans.html')

def my_follows_view(request):
    return render(request, 'profile_center/my_follows.html')
