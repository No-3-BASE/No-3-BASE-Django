from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from article.models import Article
from board.models import Section

User = get_user_model()

#搜尋結果
def search_view(request):
    keyword = request.GET.get('q', '').strip()
    articles = []
    players = []
    user = request.user

    if keyword:
        articles = Article.objects.filter(title__icontains=keyword)
        players = User.objects.filter(first_name__icontains=keyword)
    else:
        message = '請輸入搜尋關鍵字'
        
    return render(request, 'search/search.html',{
        'isLogin': request.user.is_authenticated,
        'user': user,
        'keyword': keyword,
        'players': players,
        'player_count': players.count() if players else 0,
        'articles': articles,
        'article_count': articles.count() if articles else 0
    })

def section_search_view(request, section_id):
    keyword = request.GET.get('q', '').strip()
    articles = []
    user = request.user

    section = get_object_or_404(Section, id=section_id)

    if keyword:
        articles = Article.objects.filter(title__icontains=keyword, section=section)
    else:
        message = '請輸入搜尋關鍵字'
    return render(request, 'search/section_search.html',{
        'id': section_id,
        'sectionName': section.name,
        'isLogin': request.user.is_authenticated,
        'user': user,
        'keyword': keyword,
        'articles': articles,
        'article_count': articles.count() if articles else 0
    })