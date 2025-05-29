from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_POST
from django.conf import settings
from board.models import Section
from .models import Article
from section.models import Category
from board.models import Section
import os
#建立文章
@login_required
def article_create_view(request, section_id=None):
    sections = Section.objects.all()

    if request.method == 'POST':
        print("收到POST")
        action = request.POST.get('action')

        if action == 'draft':
            section_id = request.POST.get('section')
            category_id = request.POST.get('category')
            title = request.POST.get('title')
            content = request.POST.get('content')

            section = get_object_or_404(Section, id=section_id)
            category = get_object_or_404(Category, id=category_id)

            Article.objects.create(
                status='draft',
                author=request.user,
                section=section,
                category=category,
                title=title,
                content=content
            )

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
                content=content
            )
            return redirect('profileCenter:myArticle')

    return render(request, 'article/edit_article.html', {
        'sections': sections,
        'section': None
    })

#草稿編輯
@login_required
def draft_edit_view(request, draft_id):
    return render(request, 'article/edit_article.html')

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