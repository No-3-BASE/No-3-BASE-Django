from datetime import datetime, timezone
from django.db.models import Q
from player.models import Profile
from notification.models import Notification
from article.models import Article
from chat.models import ChatRoom, Message
import math

def toolbar_context(request):
    print(f"目前登入狀態 {request.user.is_authenticated}")
    if request.user.is_authenticated:
        user = request.user
        now = datetime.now(timezone.utc)

        notifies = None

        profile = None

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = None

        try:
            notifies = Notification.objects.filter(recipient=user).order_by('-createAt')[:20]
        except Notification.DoesNotExist:
            notifies = None

        rooms = ChatRoom.objects.filter(Q(playerA=user) | Q(playerB=user)).order_by('-createAt')[:10]

        chatRooms = []

        for room in rooms:
            message = Message.objects.filter(room=room).order_by('-createAt').first()
            player = room.playerA if room.playerB == user else room.playerB
            if message:
                chatRooms.append({'message': message, 'player': player, 'sender': False if message.sender == user else True})

        article_count = Article.objects.filter(author=user, status='published').count()

        return {
            'toolBar': {
                'isLogin': True,
                'notifies': notifies,
                'id': user.id,
                'name': user.first_name,
                'profile': profile,
                'article': article_count,
                'chatRooms': chatRooms
            }
        }
    
    return {
        'toolBar': {
            'isLogin': False,
            'notify': None,
            'id': None,
            'name': "訪客",
            'profile': None,
            'article': None,
            'chatRooms': None
        }
    }