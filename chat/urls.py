from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('list/', views.chat_list_view, name='list'),
    path('player/<uuid:player_id>/', views.chatroom_view, name='room'),
    path('history/player/<uuid:player_id>/', views.chat_history, name='history'),
    path('latest/player/<uuid:player_id>/', views.load_latest, name='load'),
    path('send/player/<uuid:player_id>/', views.chat_send, name='send')
]