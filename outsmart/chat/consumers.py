from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from channels.auth import get_user, logout
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(WebsocketConsumer):

    # Connect to a room
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        user = self.scope['user']
        if user.is_authenticated:
          async_to_sync(self.channel_layer.group_add)(
              user.username,
              self.channel_name
          )

        self.accept()

    # Leave room group
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        # Show who sent the message
        if user.is_authenticated:
            message = user.username + ': ' + message
        else:
            message = 'Anonymous: ' + message
        
        msg = Message.objects.create(roomName=self.room_name, content=message, sender=user.username)
        msg.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'green': user.username
            }
        )
        

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        green = event['green']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': green
        }))
    
    # Receive message from username group
    def logout_message(self, event):
        self.send(text_data=json.dumps({
            'message': event['message']
        }))
        self.close()



