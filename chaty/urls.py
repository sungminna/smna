from django.urls import path, include

from . import admin
from .views import base_views, chatroom_views

app_name = 'chaty'

urlpatterns = [
    path('', base_views.index, name='index'),
    path('chatroom_list/', chatroom_views.chatroom_list, name='chatroom_list'),
    path('chatroom/create', chatroom_views.chatroom_create, name='chatroom_create'),
    path('chatroom/join', chatroom_views.chatroom_join, name='chatroom_join'),
    path('chatroom/<int:chatroom_id>', chatroom_views.chatroom_chat, name='chatroom_chat'),
]