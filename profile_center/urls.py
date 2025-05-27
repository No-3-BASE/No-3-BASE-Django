from django.urls import path
from . import views

app_name = 'profileCenter'

urlpatterns = [
    path('', views.player_profile_view, name='playerProfile'),
    path('edit_profile/', views.edit_profile_view, name='editProfile'),
    path('edit_privacy/', views.edit_privacy_view, name='editPrivacy'),
    path('edit_game/', views.edit_game_view, name='editGame'),
    path('daily_mission/', views.daily_mission_view, name='dailyMission'),
    path('my_article/', views.my_article_view, name='myArticle'),
    path('my_draft/', views.my_draft_view, name='myDraft'),
    path('my_bookmark/', views.my_bookmark_view, name='myBookmark'),
    path('my_fans/', views.my_fans_view, name='myFans'),
    path('my_follows/', views.my_follows_view, name='myFollows'),
]