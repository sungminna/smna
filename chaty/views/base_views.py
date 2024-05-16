from django.shortcuts import render
from ..models import Chatroom
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    return render(request, 'chaty/landing.html')


def chatroom_list(request):
    chatroom_list = Chatroom.objects.order_by('-creationtime')
    page = request.GET.get('page', '1')
    if chatroom_list:
        chatroom_list = chatroom_list.filter(
            Q(chat__participant=request.user)
        ).distinct()
    paginator = Paginator(chatroom_list, 10)
    page_obj = paginator.get_page(page)
    context = {'chatroom_list': page_obj}

    return render(request, 'chaty/chatroom_list.html', context)
