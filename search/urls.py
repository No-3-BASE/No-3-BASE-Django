from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('result/', views.search_view, name='result'),
    #path('section/<uuid:section_id>/result/', views.section_search_view, name='result'),
]