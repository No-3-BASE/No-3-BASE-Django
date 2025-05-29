from django.urls import path
from . import views

app_name = 'section'

urlpatterns = [
    path('<uuid:section_id>/', views.section_view, name='section'),
    path('<uuid:section_id>/article/<uuid:article_id>/', views.section_view, name='article'),
    path('<uuid:section_id>/article/<uuid:article_id>/edit/', views.section_view, name='editArticle'),
]