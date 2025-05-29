from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from board.models import Section
#板塊顯示
def section_view(request, section_id):
    detail = get_object_or_404(Section, id=section_id)

    return render(request, 'section/section.html', {'detail': detail})

#文章編輯
@login_required
def article_edit_view(request, article_id):
    return render(request, 'article/edit_article.html')