from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import ChatRoom, Message

User = get_user_model()

@login_required
def chat_list_view(request):
    return render(request, 'chat/message_list.html')

@login_required
def chatroom_view(request, player_id):
    player = get_object_or_404(User, pk=player_id)
    return render(request, 'chat/chat.html', {
        'player': player
    })
