from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
@login_required
def notification_list_view(request):
    user = request.user
    messages = Notification.objects.filter(recipient=user).order_by('-createAt')
    return render (request, 'notification/message_list.html',{
        'messages': messages
    })
