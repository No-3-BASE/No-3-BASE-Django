from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('list/', views.chat_list_view, name='list'),
    path('player/<uuid:player_id>/', views.chatroom_view, name='room')
]