from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from .models import Message
from django.contrib import messages

# Entry to a room
def entry(request):
    return render(request,'chat/entry.html')

# Chatroom for the user
def room(request, room_name=None):
    # Check if user exists
    if User.objects.filter(username=room_name).exists():
        context = {
            'msgs': Message.objects.filter(roomName = room_name),
            'room_name': room_name}
        return render(request, 'chat/room.html', context)
    else:
        messages.error(request, 'User does not exist')
        return render(request, 'chat/entry.html')

