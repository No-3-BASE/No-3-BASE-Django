from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Follow, Notification

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Notification)