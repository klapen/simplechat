import json
import datetime
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message

import chat.tasks as bots

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    text_commands = {
        'stock': bots.getStockQuote
    }

    def parse_to_json(self, msg):
        return {
            'author': msg.author.username,
            'content': msg.content,
            'timestamp': str(msg.timestamp)
        }

    def messages_to_json(self, messages):
        result = []
        for msg in messages:
            result.append(self.parse_to_json(msg))
        return result

    def fetch_messages(self, data):
        messages = Message.last_50_messages(self.room_group_name)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def user_message(self, msg, author):
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
            room = self.room_group_name,
            author = author_user,
            content = msg
        )
        content = {
            'command': 'new_message',
            'message': self.parse_to_json(message)
        }
        return self.send_chat_message(content)
        
    def command_message(self, msg, author):
        cmd = msg[1:].split('=')[0]
        payload = msg[1:].split('=')[1]

        if cmd in self.text_commands:
            return self.text_commands[cmd].delay(self.room_group_name, payload)
        else:
            return self.user_message(msg, author)
        
    def new_message(self, data):
        msg = data['message']
        author = data['from']
        
        if(msg[0] == '/'):
            self.command_message(msg, author)
        else:
            return self.user_message(msg, author)

    def bot_message(self, data):
        msg = data['data']
        content = {
            'command': 'new_message',
            'message' : {
                'author': msg['from'],
                'content': msg['message'],
                'timestamp' : str(datetime.datetime.now())
            }
        }
        return self.send_chat_message(content)
    
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'bot_message': bot_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

