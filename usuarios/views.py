from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Usuarios
from .validators import username_validator, password_validator

@login_required(login_url='login')
def usuariosEditarView(request, pk):
    if request.method == 'POST':
        try:
            usuario = Usuarios.objects.filter(pk=pk)
            if not usuario.exists():
                messages.add_message(request, messages.ERROR, 'Usuario não encontrado!')
                raise usuario.first().DoesNotExist
            usuario = usuario.first()

            username = username_validator(request.POST.get('username'))
            try: new_password = password_validator(request.POST.get('new-password'))
            except: new_password = None
            try: confirm_password = password_validator(request.POST.get('confirm-password'))
            except: confirm_password = None

            usuario.username = username
            if new_password and confirm_password:
                if new_password != confirm_password:
                    raise ValidationError('Campos de senha precisam ser iguais!')
                if not check_password(new_password, usuario.password):
                    usuario.set_password(new_password)
            usuario.save()
        except Exception as e:
            messages.add_message(request, messages.ERROR, e.args[0])
        return redirect(reverse('usuarios_editar', kwargs={'pk': pk}))
    if request.method == 'GET':
        usuario = Usuarios.objects.get(pk=pk)
        return render(request, 'usuarios_editar.html', {'usuario': usuario})

@login_required(login_url='login')
def usuariosDeletarView(request, pk):
    try:
        usuario = Usuarios.objects.get(pk=pk, cargo='M')
        usuario.delete()
    except Usuarios.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Usuario não encontrado!')
    return redirect(reverse('usuarios'))

@login_required(login_url='login')
def usuariosCadastroView(request):
    if request.method == 'POST':
        try:
            username = username_validator(request.POST.get('username'))
            password = password_validator(request.POST.get('password'))
            cargo = request.POST.get('cargo')

            usuario = Usuarios(username=username, cargo=cargo)
            usuario.set_password(password)
            usuario.save()
        except Exception as e:
            messages.add_message(request, messages.ERROR, e.args[0])
        else:
            messages.add_message(request, messages.SUCCESS, 'Usuario cadastrado com sucesso!')
        return redirect(reverse('usuarios'))
    if request.method == 'GET':
        return render(request, 'usuarios_cadastro.html')
    
@login_required(login_url='login')
def usuariosView(request):
    if request.method == 'POST':
        usuarios = Usuarios.objects.filter(username__icontains=request.POST.get('username_busca'), cargo='M')
        return render(request, 'usuarios.html', {'usuarios': usuarios})
    if request.method == 'GET':
        return render(request, 'usuarios.html', {'usuarios': Usuarios.objects.filter(cargo='M')})

def loginView(request):
    if request.method == 'POST':
        try:
            username = username_validator(request.POST.get('login'))
            password = username_validator(request.POST.get('senha'))
            usuario = authenticate(username=username, password=password)
            if not usuario:
                raise ValidationError('Login ou senha inválidos!')
            login(request, usuario)
        except Exception as e:
            messages.add_message(request, messages.ERROR, e.args[0])
        else:
            return redirect(reverse('usuarios'))
        finally:
            return redirect(reverse('login'))
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('usuarios'))
        return render(request, 'login.html')

def logoutView(request):
    request.session.flush()
    return redirect(reverse('login'))