from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from datetime import datetime, timezone
from django.http import JsonResponse
from django.templatetags.static import static
from django.contrib.contenttypes.models import ContentType
from board.models import Section
from article.models import Article, Comment, Like, Favorite

User = get_user_model()

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
    comments = article.comments.filter(approved=True).order_by('createAt')#[:10]動態載入擴充
    commentFloor = {
        str(comment.id): idx + 1
        for idx, comment in enumerate(comments)
    }
    
    isLike = False
    content_type = ContentType.objects.get_for_model(article)
    
    if request.user.is_authenticated:
        isLike = Like.objects.filter(player=request.user, contentType=content_type, objectId=article.id).exists()
        isMark = Favorite.objects.filter(player=request.user, article=article).exists()

    return render(request, 'section/article.html', {
        'article': article,
        'isMark': isMark,
        'isLike': isLike,
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

    #每日文章經驗
    try:
        profile = user.profile
        now = datetime.now(timezone.utc).date()

        if profile.messageExpGainDate != now:
            profile.exp += 15
            profile.messageExpGainDate = now

        profile.recalculate_level()
        profile.save()
    except User.DoesNotExist:
        pass

    if parent_id:
        parent = Comment.objects.filter(id=parent_id).first()
        parentFloor = article.comments.filter(approved=True, createAt__lte=parent.createAt).count()

    comment = Comment.objects.create(article=article, author=user, content=content, parentComment=parent, approved=request.user.is_authenticated)

    comment_count = Comment.objects.filter(article=article, approved=True).count()
    comment_score = comment_count * 5
    like_score = article.like * 3
    bookmark_score = article.bookmark
    article.comment = comment_count
    article.hot = comment_score + like_score + bookmark_score
    article.save()

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

#按讚處理
@login_required
@require_POST
def article_like_toggle(request, section_id, article_id):
    user = request.user
    article = get_object_or_404(Article, id=article_id)
    
    content_type = ContentType.objects.get_for_model(article)
    
    #檢查是否按讚
    existing_like = Like.objects.filter(player=user, contentType=content_type, objectId=article.id).first()
    
    if existing_like:
        #取消按讚
        existing_like.delete()
        article.like = max(article.like - 1, 0)
        liked = False
    else:
        #新增按讚
        Like.objects.create(player=user, contentType=content_type, objectId=article.id,)
        article.like += 1
        liked = True

        #每日按讚經驗
        try:
            profile = user.profile
            now = datetime.now(timezone.utc).date()

            if profile.likeExpGainDate != now:
                profile.exp += 10
                profile.likeExpGainDate = now

            profile.recalculate_level()
            profile.save()
        except User.DoesNotExist:
            pass

    comment_count = Comment.objects.filter(article=article, approved=True).count()
    comment_score = comment_count * 5
    like_score = article.like * 3
    bookmark_score = article.bookmark
    article.comment = comment_count
    article.hot = comment_score + like_score + bookmark_score
    article.save()
    
    return JsonResponse({'success': True, 'liked': liked})

#收藏處理
@login_required
@require_POST
def article_mark_toggle(request, section_id, article_id):
    user = request.user
    article = get_object_or_404(Article, id=article_id)
    
    content_type = ContentType.objects.get_for_model(article)
    
    #檢查是否收藏
    existing_mark = Favorite.objects.filter(player=user, article=article).first()
    
    if existing_mark:
        #取消收藏
        existing_mark.delete()
        article.bookmark = max(article.bookmark - 1, 0)
        marked = False
    else:
        #新增收藏
        Favorite.objects.create(player=user, article=article)
        article.bookmark += 1
        marked = True
    
    comment_count = Comment.objects.filter(article=article, approved=True).count()
    comment_score = comment_count * 5
    like_score = article.like * 3
    bookmark_score = article.bookmark
    article.comment = comment_count
    article.hot = comment_score + like_score + bookmark_score
    article.save()
    
    return JsonResponse({'success': True, 'marked': marked})