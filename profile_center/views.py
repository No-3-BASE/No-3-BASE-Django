from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.http import require_POST
from django.urls import reverse
from player.models import Profile, Follow
from article.models import Article, Favorite
from board.models import Section
from .models import GameCard
import json
import uuid
#用戶資料
@login_required
def player_profile_view(request):
    user = request.user

    try:
        profile = Profile.objects.get(player=user)
    except Profile.DoesNotExist:
        profile = None

    games = GameCard.objects.filter(player=user)
    absolute_url = request.build_absolute_uri(reverse('player:gameCard', args=[user.id]))

    return render(request, 'profile_center/player_profile.html', {
        'id': user.id,
        'name': user.first_name,
        'account': user.username,
        'email': user.email,
        'join': user.date_joined.strftime('%Y-%m-%d'),
        'profile': profile,
        'url': absolute_url,
        'games': games
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
    user = request.user
    cards = GameCard.objects.filter(player=user)

    card_data = []
    for card in cards:
        card_data.append({
            "uid": card.uid,
            "section": card.section.name if card.section else "",
            "id": card.section.id if card.section else "",
            "customName": card.customName if not card.section else "",
        })
    
    try:
        profile = Profile.objects.get(player=user)
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'profile_center/edit_game.html', {
        'name': user.first_name,
        'profile': profile,
        "cards": card_data
    })

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

    sortBy = request.GET.get("sort", "time")

    if sortBy == "hot":
        publishedArticles = Article.objects.filter(author=user, status='published').order_by('-hot', '-publishAt')
    else:
        publishedArticles = Article.objects.filter(author=user, status='published').order_by('-publishAt')

    return render(request, 'profile_center/my_article.html', {
        'name': user.first_name,
        'profile': profile,
        'sortBy': sortBy,
        'articles': publishedArticles
    })

#我的草稿
@login_required
def my_draft_view(request):
    user = request.user

    try:
        profile = Profile.objects.get(player=user)
    except Profile.DoesNotExist:
        profile = None

    draftArticles = Article.objects.filter(author=user, status='draft').order_by('-lastEdit')

    return render(request, 'profile_center/my_draft.html', {
        'name': user.first_name,
        'profile': profile,
        'articles': draftArticles
    })

#我的收藏
@login_required
def my_bookmark_view(request):
    user = request.user

    try:
        profile = Profile.objects.get(player=user)
    except Profile.DoesNotExist:
        profile = None

    sortBy = request.GET.get("sort", "time")

    if sortBy == "hot":
        bookmarkArticles = Article.objects.filter(favorites__player=user, status='published').distinct().order_by('-hot', '-publishAt')
    else:
        bookmarkArticles = Article.objects.filter(favorites__player=user, status='published').distinct().order_by('-publishAt')

    return render(request, 'profile_center/my_bookmark.html', {
        'name': user.first_name,
        'profile': profile,
        'sortBy': sortBy,
        'articles': bookmarkArticles
    })

#我的粉絲
@login_required
def my_fans_view(request):
    user = request.user

    try:
        profile = Profile.objects.get(player=user)
    except Profile.DoesNotExist:
        profile = None

    followers = Follow.objects.filter(following=user).select_related('follower')
    return render(request, 'profile_center/my_fans.html', {
        'name': user.first_name,
        'profile': profile,
        'follows': followers
    })

#我的關注
@login_required
def my_follows_view(request):
    user = request.user

    try:
        profile = Profile.objects.get(player=user)
    except Profile.DoesNotExist:
        profile = None

    followings = Follow.objects.filter(follower=user).select_related('following')
    return render(request, 'profile_center/my_follows.html', {
        'name': user.first_name,
        'profile': profile,
        'follows': followings
    })

#板塊列表
def section_list(request):
    sections = Section.objects.all().values('id', 'name')
    return JsonResponse(list(sections), safe=False)

#遊戲上傳
@login_required
@require_POST
def upload_games(request):
    data = json.loads(request.body)
    cards = data.get('cards', [])
    user = request.user

    created = []

    GameCard.objects.filter(player=user).delete()
    
    for item in cards:
        section_id = item.get('board')
        uid = item.get('uid')

        if not uid or not section_id:
            continue

        section_obj = None
        custom_name = ""

        try:
            # 先嘗試把 section_id 轉成 UUID
            section_uuid = uuid.UUID(section_id)
            # 轉成功代表它是 UUID 格式，嘗試從資料庫取 Section
            section_obj = Section.objects.get(id=section_uuid)
        except (ValueError, Section.DoesNotExist):
            # ValueError: 不是合法 UUID，或 Section 不存在
            try:
                section_obj = Section.objects.get(name=section_id)
            except (ValueError, Section.DoesNotExist):
                # 直接把 section_id 當成自訂名稱存 customName
                custom_name = section_id
                section_obj = None

        card, created_flag = GameCard.objects.get_or_create(
            player=user,
            section=section_obj,
            customName=custom_name,
            uid=uid
        )
        created.append({
            "id": str(card.id),
            "uid": card.uid,
            "section": section_obj.name if section_obj else custom_name,
            "created": created_flag
        })

    return JsonResponse({"success": True, "created": created})