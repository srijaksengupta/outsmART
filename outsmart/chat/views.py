from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from .models import Message

# Create your views here.
def entry(request):
    return render(request,'chat/entry.html')

def room(request, room_name=None):
    if User.objects.filter(username=room_name).exists():
        context = {
            'msgs': Message.objects.filter(roomName = room_name),
            'room_name': room_name}
        return render(request, 'chat/room.html', context)
    else:
        return render(request, 'chat/entry.html')

