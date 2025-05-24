from django.shortcuts import render

def player_profile_view(request):
    return render(request, 'profile_center/player_profile.html')

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
