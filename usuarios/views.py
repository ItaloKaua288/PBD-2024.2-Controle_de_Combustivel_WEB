from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from rolepermissions.decorators import has_role_decorator
from .models import Usuarios
from .validators import username_validator, password_validator

@login_required(login_url='login')
def usuariosPerfil(request, pk):
    usuario = Usuarios.objects.get(pk=pk)
    context = {'perfil_logado': usuario, 'usuario': usuario}
    if request.method == 'POST':
        try:
            new_password = password_validator(request.POST.get('new-password'))
            confirm_password = password_validator(request.POST.get('confirm-password'))
            if new_password != confirm_password:
                raise ValueError('Campos de senha precisam ser iguais!')
            if not check_password(new_password, usuario.password):
                usuario.set_password(new_password)
                usuario.save()
                messages.add_message(request, messages.SUCCESS, 'Senha alterada com sucesso!')
        except Exception as e:
            messages.add_message(request, messages.ERROR, e.args[0])
        return redirect(reverse('usuarios_perfil', kwargs={'pk': pk}))
    if request.method == 'GET':
        return render(request, 'usuarios_perfil.html', context)

@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
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
            try:
                messages.add_message(request, messages.ERROR, e.args[0])
            except:
                messages.add_message(request, messages.ERROR, e.args)
        return redirect(reverse('usuarios_editar', kwargs={'pk': pk}))
    if request.method == 'GET':
        context = {
            'perfil_logado': Usuarios.objects.get(username=request.user),
            'usuario': Usuarios.objects.get(pk=pk)
        }
        return render(request, 'usuarios_editar.html', context)

@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def usuariosDeletarView(request, pk):
    try:
        usuario = Usuarios.objects.get(pk=pk, cargo='M')
        usuario.delete()
    except Usuarios.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Usuario não encontrado!')
    return redirect(reverse('usuarios'))

@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
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
            try:
                messages.add_message(request, messages.ERROR, e.args[0])
            except:
                messages.add_message(request, messages.ERROR, e.args)
        else:
            messages.add_message(request, messages.SUCCESS, 'Usuario cadastrado com sucesso!')
        return redirect(reverse('usuarios'))
    if request.method == 'GET':
        context = {'perfil_logado': Usuarios.objects.get(username=request.user)}
        return render(request, 'usuarios_cadastro.html', context)
    
@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def usuariosView(request):
    context = {'perfil_logado': Usuarios.objects.get(username=request.user)}
    if request.method == 'POST':
        usuarios = Usuarios.objects.filter(username__icontains=request.POST.get('username_busca'), cargo='M')

        context['usuarios'] = usuarios
        return render(request, 'usuarios.html', context)
    if request.method == 'GET':
        context['usuarios'] = Usuarios.objects.filter(cargo='M')
        return render(request, 'usuarios.html', context)

@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def usuariosDesativarView(request, pk):
    usuario = get_object_or_404(Usuarios, pk=pk)
    usuario.is_active = False
    usuario.save()
    return redirect(reverse('usuarios'))

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
            if Usuarios.objects.get(username=request.user).cargo == 'A':
                return redirect(reverse('login'))
            return redirect(reverse('usuarios_perfil', kwargs={'pk':usuario.pk}))
    if request.method == 'GET':
        if request.user.is_authenticated:
            usuario = Usuarios.objects.get(username=request.user)
            if usuario.cargo == 'A':
                return redirect(reverse('usuarios'))
            return redirect(reverse('usuarios_perfil', kwargs={'pk':usuario.pk}))
        return render(request, 'login.html')

def logoutView(request):
    request.session.flush()
    return redirect(reverse('login'))