from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Message(models.Model):
    room = models.CharField(max_length=100, default='no-room')
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_50_messages(room):
        return Message.objects.order_by('-timestamp').filter(room=room)[:50]
