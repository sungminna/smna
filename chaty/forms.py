from django import forms
from chaty.models import Chatroom
from chaty.models import Message

class ChatroomForm(forms.ModelForm):
    class Meta:
        model = Chatroom
        fields = ['roomname']
        labels = {
            'roomname': 'roomname',
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {
            'message': 'message',
        }