from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import ChatRoom, Message, MessageDeletion

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

@login_required
def chat_history(request, player_id):
    page = int(request.GET.get('page', 1))
    page_size = 20
    user = request.user

    try:
        room = ChatRoom.objects.get(Q(playerA=user, playerB__id=player_id) | Q(playerB=user, playerA__id=player_id))
    except ChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)

    #找到使用者刪除時間
    deletion = MessageDeletion.objects.filter(room=room, player=user).first()
    deleteAt = deletion.deleted if deletion else None

    #取得訊息
    qs = Message.objects.filter(room=room)
    if deleteAt:
        qs = qs.filter(createAt__gt=deleteAt)

    qs = qs.order_by('-createAt')
    paginator = Paginator(qs, page_size)
    current_page = paginator.page(page)

    messages = [{
        'id': msg.id,
        'sender': msg.sender.username if msg.sender else "System",
        'content': msg.content,
        'timestamp': msg.createAt.strftime('%H:%M')
    } for msg in current_page.object_list]

    return JsonResponse({
        'messages': messages,
        'has_next': current_page.has_next()
    })
