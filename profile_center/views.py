from django.shortcuts import render, redirect
from player.models import Profile, Follow
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from article.models import Article
#用戶資料
@login_required
def player_profile_view(request):
    user = request.user

    try:
        profile = Profile.objects.get(player=user)
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'profile_center/player_profile.html', {
        'name': user.first_name,
        'account': user.username,
        'email': user.email,
        'join': user.date_joined.strftime('%Y-%m-%d'),
        'profile': profile
    })

#編輯隱私
@login_required
def edit_privacy_view(request):
    return render(request, 'profile_center/edit_privacy.html')

#編輯資料
@login_required
def edit_profile_view(request):
    user = request.user

    try:
        profile = Profile.objects.get(player=user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        name = request.POST.get('name')
        birthday = request.POST.get('birthday')
        slogan = request.POST.get('slogan')

        user.first_name = name
        user.save()

        profile.birthday = birthday
        profile.slogan = slogan

        photo = request.FILES.get('photo')
        if photo:
            if profile.photo and default_storage.exists(profile.photo.name):
                default_storage.delete(profile.photo.name)
            profile.photo = photo

        profile.save()

        return redirect('profileCenter:playerProfile')

    return render(request, 'profile_center/edit_profile.html', {
        'name': user.first_name,
        'account': user.username,
        'email': user.email,
        'join': user.date_joined.strftime('%Y-%m-%d'),
        'profile': profile
    })

#編輯遊戲
@login_required
def edit_game_view(request):
    return render(request, 'profile_center/edit_game.html')

#每日任務
@login_required
def daily_mission_view(request):
    user = request.user

    try:
        profile = Profile.objects.get(player=user)
    except Profile.DoesNotExist:
        profile = None

    tasksStatus = profile.get_daily_tasks_status()

    return render(request, 'profile_center/daily_mission.html', {
        'name': user.first_name,
        'profile': profile,
        'tasks': tasksStatus
    })

#我的文章
@login_required
def my_article_view(request):
    user = request.user

    try:
        profile = Profile.objects.get(player=user)
    except Profile.DoesNotExist:
        profile = None

    publishedArticles = Article.objects.filter(author=request.user, status='published')

    return render(request, 'profile_center/my_article.html', {
        'name': user.first_name,
        'profile': profile,
        'articles': publishedArticles
    })

#我的草稿
@login_required
def my_draft_view(request):
    return render(request, 'profile_center/my_draft.html')

#我的收藏
@login_required
def my_bookmark_view(request):
    return render(request, 'profile_center/my_bookmark.html')

#我的粉絲
@login_required
def my_fans_view(request):
    user = request.user

    followers = Follow.objects.filter(following=user).select_related('follower')
    return render(request, 'profile_center/my_fans.html', {
        'followers': followers
    })

#我的關注
@login_required
def my_follows_view(request):
    user = request.user

    followings = Follow.objects.filter(follower=user).select_related('following')
    return render(request, 'profile_center/my_follows.html', {
        'followings': followings
    })
