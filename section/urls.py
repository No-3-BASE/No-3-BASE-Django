from django.urls import path
from . import views

app_name = 'section'

urlpatterns = [
    path('<uuid:section_id>/', views.section_view, name='section'),
    path('<uuid:section_id>/article/<uuid:article_id>/', views.article_view, name='article'),
    path('<uuid:section_id>/article/<uuid:article_id>/edit/', views.article_edit_view, name='editArticle'),
    path('<uuid:section_id>/article/<uuid:article_id>/comment/', views.upload_comment, name='comment'),
    path('<uuid:section_id>/article/<uuid:article_id>/like_toggle/', views.article_like_toggle, name='articleLike'),
    path('<uuid:section_id>/article/<uuid:article_id>/mark_toggle/', views.article_mark_toggle, name='articleMark')
    
]