from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Usuarios

def usuariosView(request):
    if request.method == 'POST':
        usuarios = Usuarios.objects.filter(username__icontains=request.POST.get('username_busca'), cargo='M')
        return render(request, 'usuarios.html', {'usuarios': usuarios})
    if request.method == 'GET':
        return render(request, 'usuarios.html', {'usuarios': Usuarios.objects.filter(cargo='M')})

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('senha')
        usuario = authenticate(username=username, password=password)
        if not usuario:
            messages.add_message(request, messages.ERROR, 'Login ou senha inválidos!')
            return redirect(reverse('login'))
        login(request, usuario)
        return redirect(reverse('usuarios'))
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('usuarios'))
        return render(request, 'login.html')

def logoutView(request):
    request.session.flush()
    return redirect(reverse('login'))