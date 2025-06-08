from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import timedelta
from .models import ChatRoom, Message, MessageDeletion
import json

User = get_user_model()

@login_required
def chat_list_view(request):
    user = request.user
    rooms = ChatRoom.objects.filter(Q(playerA=user) | Q(playerB=user))

    chatRooms = []

    for room in rooms:
        message = Message.objects.filter(room=room).order_by('-createAt').first()
        player = room.playerA if room.playerB == user else room.playerB

        if message:
            chatRooms.append({'message': message, 'player': player, 'sender': False if message.sender == user else True})

    print(message)
    print(player)

    return render(request, 'chat/message_list.html', {
        'chatRooms': chatRooms
    })

@login_required
def chatroom_view(request, player_id):
    player = get_object_or_404(User, pk=player_id)

    if player == request.user:
        return redirect('chat:list')
    
    return render(request, 'chat/chat.html', {
        'player': player
    })

#載入歷史訊息
@login_required
def chat_history(request, player_id):
    page = int(request.GET.get('page', 1))
    page_size = 20
    user = request.user

    try:
        other_user = User.objects.get(id=player_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'user not found'}, status=404)

    try:
        room = ChatRoom.objects.get(Q(playerA=user, playerB__id=player_id) | Q(playerB=user, playerA__id=player_id))
    except ChatRoom.DoesNotExist:
        ChatRoom.objects.create(playerA=user, playerB=other_user)
        return JsonResponse({'error': 'create room'}, status=404)

    #找到使用者刪除時間
    deletion = MessageDeletion.objects.filter(room=room, player=user).first()
    deleteAt = deletion.deleted if deletion else None

    #取得訊息
    qs = Message.objects.filter(room=room)
    if deleteAt:
        qs = qs.filter(createAt__gt=deleteAt)

    qs = qs.order_by('createAt')
    paginator = Paginator(qs, page_size)
    current_page = paginator.page(page)

    messages = [{
        'id': msg.id,
        'sender': msg.sender.username if msg.sender else None,
        'content': msg.content,
        'timestamp': (msg.createAt + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M')
    } for msg in current_page.object_list]

    return JsonResponse({
        'messages': messages,
        'has_next': current_page.has_next()
    })

#發送訊息
@login_required
def chat_send(request, player_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    user = request.user

    try:
        other_user = User.objects.get(id=player_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'user not found'}, status=404)

    try:
        room = ChatRoom.objects.get(Q(playerA=user, playerB__id=player_id) | Q(playerB=user, playerA__id=player_id))
    except ChatRoom.DoesNotExist:
        ChatRoom.objects.create(playerA=user, playerB=other_user)
        return JsonResponse({'error': 'create room'}, status=404)
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        if not content:
            return JsonResponse({'error': 'Empty content'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # 建立訊息
    msg = Message.objects.create(
        room=room,
        sender=user,
        content=content
    )

    return JsonResponse({'success': True, 'message_id': msg.id})

#載入最新訊息
@login_required
def load_latest(request, player_id):
    user = request.user
    after_id = request.GET.get('after_id')

    try:
        other_user = User.objects.get(id=player_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'user not found'}, status=404)
    
    try:
        room = ChatRoom.objects.get(Q(playerA=user, playerB__id=player_id) | Q(playerB=user, playerA__id=player_id))
    except ChatRoom.DoesNotExist:
        ChatRoom.objects.create(playerA=user, playerB=other_user)
        return JsonResponse({'error': 'create room'}, status=404)

    messages_qs = Message.objects.filter(room=room).order_by('createAt')  # 由舊到新

    if after_id:
        try:
            after_id = int(after_id)
            messages_qs = messages_qs.filter(id__gt=after_id)
        except ValueError:
            pass  # 如果傳來的 after_id 不是整數就忽略

    messages = [{
        'id': msg.id,
        'sender': msg.sender.username if msg.sender else None,
        'content': msg.content,
        'timestamp': (msg.createAt + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M')  # +8小時時區修正
    } for msg in messages_qs]

    return JsonResponse({'messages': messages})