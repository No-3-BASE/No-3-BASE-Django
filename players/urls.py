from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup_view, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('welcome', views.consent_form_view, name='welcome'),
    path('login', views.login_view, name='login'),
]