from django.contrib import messages

from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


from ..forms import ChatroomForm, MessageForm
from ..models import Chatroom
from ..models import Chat
from ..models import Message

@login_required(login_url='common:login')
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

@login_required(login_url='common:login')
def chatroom_create(request):
    #create chatroom
    if request.method == 'POST':
        form = ChatroomForm(request.POST)
        if form.is_valid():
            chatroom = form.save(commit=False)
            chatroom.creationtime = timezone.now()
            chatroom.save()

            chat = Chat()
            chat.chatroom = chatroom
            chat.participant = request.user
            chat.save()
            return redirect('chaty:index')
    #show chatroom
    else:
        form = ChatroomForm()
    context = {'form': form}
    return render(request, 'chaty/chatroom_create_form.html', context)


@login_required(login_url='common:login')
def chatroom_join(request):
    if request.method == 'POST':
        roomname = request.POST['roomname']
        chatroom = Chatroom.objects.filter(roomname=roomname)
        if not chatroom.exists():
            messages.error(request, 'Room does not exist')
            return render(request, 'chaty/chatroom_join_form.html')
        else:
            ###수정중
            chat_db = Chat.objects.get(chatroom=chatroom.get())
            print(chat_db)
            if chat_db:
                return redirect('chaty:chatroom_chat', chatroom_id=chatroom.get().id)

            chat = Chat()
            chat.chatroom = chatroom.get()
            chat.participant = request.user
            chat.save()
            return redirect('chaty:chatroom_chat', chatroom_id=chatroom.get().id)
    else:
        return render(request, 'chaty/chatroom_join_form.html')

@login_required(login_url='common:login')
def chatroom_chat(request, chatroom_id):
    #create msg
    if request.method == 'POST':
        # ajax는 나중에 해보장
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.message = form.cleaned_data['message']
            msg.sent_time = timezone.now()
            msg.viewedcnt = 1
            msg.chat = Chat.objects.get(pk=chatroom_id)
            msg.save()
            chatroom = Chatroom.objects.get(pk=chatroom_id)
            chatroom.latest_message = msg
            chatroom.save()
            return redirect('{}#msg_{}'.format(resolve_url('chaty:chatroom_chat', chatroom_id=chatroom_id), msg.id))
            #return redirect('chaty:chatroom_chat', chatroom_id=chatroom_id)
    #show msgs
    else:
        chatroom = get_object_or_404(Chatroom, pk=chatroom_id)
        participant_dict_list = list(Chat.objects.filter(chatroom_id=chatroom_id).values('participant_id'))
        participant_list = list()
        for dict in participant_dict_list:
            participant_list.append(dict['participant_id'])
        if request.user.id not in participant_list:
            return redirect('chaty:index')

        message_list = Message.objects.filter(chat__chatroom=chatroom)
        context = {"chatroom": chatroom, 'message_list': message_list, 'participant_cnt': len(participant_list)}
        return render(request, 'chaty/chatroom.html', context)