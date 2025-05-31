from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone as dj_timezone
from datetime import datetime, timezone
from board.models import Section
from section.models import Category
from board.models import Section
from .models import Article
import os

User = get_user_model()

#建立文章
@login_required
def article_create_view(request, section_id=None):
    user = request.user
    sections = Section.objects.all()

    if request.method == 'POST':
        print("收到POST")
        action = request.POST.get('action')

        if action == 'draft':
            section_id = request.POST.get('section')
            category_id = request.POST.get('category')
            title = request.POST.get('title')
            content = request.POST.get('content')

            if section_id:
                section = get_object_or_404(Section, id=section_id)
            else:
                section = None
            
            if category_id:
                category = get_object_or_404(Category, id=category_id)
            else:
                category = None

            Article.objects.create(
                status='draft',
                author=request.user,
                section=section,
                category=category,
                title=title,
                content=content
            )

            #每日草稿經驗
            try:
                profile = user.profile
                now = datetime.now(timezone.utc).date()

                if profile.draftExpGainDate != now:
                    profile.exp += 15
                    profile.draftExpGainDate = now

                profile.recalculate_level()
                profile.save()
            except User.DoesNotExist:
                pass

            return redirect('profileCenter:myDraft')
        
        if action == 'article':
            section_id = request.POST.get('section')
            category_id = request.POST.get('category')
            title = request.POST.get('title')
            content = request.POST.get('content')

            section = get_object_or_404(Section, id=section_id)
            category = get_object_or_404(Category, id=category_id)

            Article.objects.create(
                status='published',
                author=request.user,
                section=section,
                category=category,
                title=title,
                content=content,
                publishAt= dj_timezone.now()
            )
            
            #每日文章經驗
            try:
                profile = user.profile
                now = datetime.now(timezone.utc).date()

                if profile.articleExpGainDate != now:
                    profile.exp += 25
                    profile.articleExpGainDate = now

                profile.recalculate_level()
                profile.save()
            except User.DoesNotExist:
                pass

            return redirect('profileCenter:myArticle')

    return render(request, 'article/edit_article.html', {
        'sections': sections,
        'section_id': section_id,
        'article': None
    })

#草稿編輯
@login_required
def draft_edit_view(request, draft_id):
    user = request.user
    sections = Section.objects.all()

    article = get_object_or_404(Article, id=draft_id, author=user)

    if request.method == 'POST':
        print("收到POST")
        action = request.POST.get('action')

        if action == 'draft':
            print("儲存草稿")
            section_id = request.POST.get('section')
            category_id = request.POST.get('category')

            if section_id:
                section = get_object_or_404(Section, id=section_id)
            else:
                section = None
            
            if category_id:
                category = get_object_or_404(Category, id=category_id)
            else:
                category = None

            article.section = section
            article.category = category
            article.title = request.POST.get('title')
            article.content = request.POST.get('content')

            article.save()

            return redirect('profileCenter:myDraft')
        
        if action == 'article':
            print("發布文章")
            section_id = request.POST.get('section')
            category_id = request.POST.get('category')

            section = get_object_or_404(Section, id=section_id)
            category = get_object_or_404(Category, id=category_id)

            article.section = section
            article.category = category
            article.title = request.POST.get('title')
            article.content = request.POST.get('content')
            article.status = 'published'
            article.publishAt = dj_timezone.now()

            article.save()

            #每日文章經驗
            try:
                profile = user.profile
                now = datetime.now(timezone.utc).date()

                if profile.articleExpGainDate != now:
                    profile.exp += 25
                    profile.articleExpGainDate = now

                profile.recalculate_level()
                profile.save()
            except User.DoesNotExist:
                pass

            return redirect('profileCenter:myArticle')

    return render(request, 'article/edit_article.html', {
        'sections': sections,
        'article': article
    })

#請求分類
def load_categories(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseForbidden("不允許直接訪問這個連結")

    section_id = request.GET.get('section_id')
    categories = Category.objects.filter(section_id=section_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

#圖片上傳
@login_required
@require_POST
def upload_image(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseForbidden("不允許直接訪問這個連結")

    image_file = request.FILES.get('image')
    if not image_file:
        return JsonResponse({'error': '沒有上傳圖片'}, status=400)

    ext = os.path.splitext(image_file.name)[1]
    random_name = get_random_string(16) + ext

    upload_path = os.path.join(settings.MEDIA_ROOT, 'article_image', random_name)
    print(f"建立儲存路徑{upload_path}")

    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
    print("確保資料夾存在")

    with open(upload_path, 'wb+') as dest:
        for chunk in image_file.chunks():
            dest.write(chunk)
    print("寫入檔案")

    image_url = settings.MEDIA_URL + 'article_image/' + random_name
    print(f"公開訪問連結{image_url}")

    return JsonResponse({'url': image_url})
