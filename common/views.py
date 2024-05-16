from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from common.forms import UserFrom

# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        form = UserFrom(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserFrom()
    return render(request, 'common/signup.html', {'form': form})

