from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib import messages

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('senha')
        usuario = authenticate(username=username, password=password)
        if not usuario:
            messages.add_message(request, messages.ERROR, 'Login ou senha inválidos!')
            return redirect(reverse('login'))
        login(request, usuario)
        return render(request, 'test.html')
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'test.html')
        return render(request, 'login.html')

def logoutView(request):
    request.session.flush()
    return redirect(reverse('login'))