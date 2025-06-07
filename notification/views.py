from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def notification_list_view(request):
    return render (request, 'notification/message_list.html')
