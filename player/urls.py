from django.urls import path
from . import views

app_name = 'player'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('welcome/', views.consent_form_view, name='welcome'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<uuid:player_id>/', views.profile_view, name='profile'),
    path('follow_toggle/', views.follow_toggle, name='followToggle'),
    path('game_card/<uuid:player_id>/', views.game_card_view, name='gameCard')
]