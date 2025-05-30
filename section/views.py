from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.templatetags.static import static
from board.models import Section
from article.models import Article, Comment
#板塊顯示
def section_view(request, section_id):
    section = get_object_or_404(Section, id=section_id)

    sortBy = request.GET.get("sort", "time")

    if sortBy == "hot":
        articles = Article.objects.filter(section=section, status='published').order_by('-hot', '-publishAt')
    else:
        articles = Article.objects.filter(section=section, status='published').order_by('-publishAt')

    return render(request, 'section/section.html', {
        'section': section,
        'sortBy': sortBy,
        'articles': articles
    })

def article_view(request, section_id, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comments.filter(approved=True).order_by('createAt')[:10]
    commentFloor = {
        str(comment.id): idx + 1
        for idx, comment in enumerate(comments)
    }

    return render(request, 'section/article.html', {
        'article': article,
        'comments': comments,
        'commentFloor': commentFloor
    })

#文章編輯
@login_required
def article_edit_view(request, article_id):
    return render(request, 'article/edit_article.html')

#留言上傳
@require_POST
def upload_comment(request, section_id, article_id):
    user = request.user if request.user.is_authenticated else None
    content = request.POST.get('comment')
    parent_id = request.POST.get('parent')

    if not content or content.strip() == '':
        return JsonResponse({'error': "訊號無效：請輸入有效內容以啟動傳輸"})
    
    article = get_object_or_404(Article, id=article_id)

    parent = None
    parentFloor = None

    if parent_id:
        parent = Comment.objects.filter(id=parent_id).first()
        parentFloor = article.comments.filter(approved=True, createAt__lte=parent.createAt).count()

    comment = Comment.objects.create(article=article, author=user, content=content, parentComment=parent, approved=request.user.is_authenticated)

    authorPhoto = static('assets/images/No3BASE.png')
    if comment.author and hasattr(comment.author, 'profile') and comment.author.profile.photo:
        authorPhoto = comment.author.profile.photo.url

    return JsonResponse({
        'id': str(comment.id),
        'author': comment.author.first_name if comment.author else "未識別訪客",
        'authorDays': comment.author.profile.signupDays if comment.author and hasattr(comment.author, 'profile') else 0,
        'authorLevel': comment.author.profile.level if comment.author and hasattr(comment.author, 'profile') else "-",
        'authorSlogan': comment.author.profile.slogan if comment.author and hasattr(comment.author, 'profile') else "未識別的訪客不曾在此留下痕跡",
        'authorPhoto': authorPhoto,
        'content': comment.content if comment.author else "評論審核中",
        'createAt': comment.createAt.strftime("%Y-%m-%d %H:%M"),
        'floor': comment.floor if comment.author else 0,
        'parentId': parent_id,
        'parentFloor': parentFloor
    })