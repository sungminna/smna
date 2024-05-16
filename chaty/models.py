from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Chatroom(models.Model):
    roomname = models.CharField(max_length=50, unique=True)
    latest_message = models.ForeignKey("Message", on_delete=models.CASCADE, null=True, default=None)
    creationtime = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey("Chatroom", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('participant', 'chatroom')

class Message(models.Model):
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE, default=None)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    message = models.TextField()
    senttime = models.DateTimeField(auto_now_add=True)
    viewedcnt = models.IntegerField(default=0)

