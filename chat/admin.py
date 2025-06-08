from django.contrib import admin
from .models import ChatRoom, Message, MessageDeletion

admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(MessageDeletion)