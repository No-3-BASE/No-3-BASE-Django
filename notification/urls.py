from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('list/', views.notification_list_view, name='list')
]