from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from board.models import Section
from article.models import Article
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

def article_view(request, article_id):
    return render

#文章編輯
@login_required
def article_edit_view(request, article_id):
    return render(request, 'article/edit_article.html')