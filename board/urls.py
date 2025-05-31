from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('rules', views.rule_view, name='rule')
]