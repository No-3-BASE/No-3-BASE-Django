from django.urls import path
from . import views

app_name = 'section'

urlpatterns = [
    path('<uuid:section_id>/', views.section_view, name='section'),
]