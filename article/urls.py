from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('draft/<uuid:draft_id>/edit/', views.draft_edit_view, name='editDraft'),
    path('create/', views.article_create_view, name='create'),
    path('ajax/load_categories/', views.load_categories, name='ajaxCategories'),
    path('ajax/upload_image/', views.upload_image, name='uploadImage')
]