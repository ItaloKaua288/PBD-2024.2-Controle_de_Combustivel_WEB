from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, View
from rolepermissions.decorators import has_role_decorator
from .models import Usuarios
from .forms import UsuariosForm, LoginForm
from utils.utils import HasRoleMixinCustom

class Motoristas_view(LoginRequiredMixin, HasRoleMixinCustom, ListView):
    """
    Exibe a lista de motoristas, com suporte a busca.
    """
    model = Usuarios
    template_name = 'motoristas_listar.html'
    login_url = reverse_lazy('login')
    paginate_by = 10
    allowed_roles = ['administrador']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cadastro_form'] = UsuariosForm()
        return context

    def get_queryset(self):
        busca = self.request.GET.get('busca', '')
        queryset = Usuarios.objects.filter(cargo='M', username__icontains=busca)
        return queryset

class Usuario_cadastrar_view(LoginRequiredMixin, HasRoleMixinCustom, CreateView):
    """
    View para cadastrar novos usuarios.
    """
    model = Usuarios
    form_class = UsuariosForm
    template_name = 'base_CRUD.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('motoristas')
    allowed_roles = ['administrador']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_titulo"] = 'Cadastrar'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuario adicionado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

class Usuario_editar_view(LoginRequiredMixin, HasRoleMixinCustom, UpdateView):
    """
    Edita as informações de um usuario existente.
    """
    model = Usuarios
    form_class = UsuariosForm
    template_name = 'base_CRUD.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('motoristas')
    allowed_roles = ['administrador']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_titulo"] = 'Editar'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Usuario atualizado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def usuarios_desativar_view(request, pk):
    """
    Ativa ou desativa um usuario existente.
    """
    usuario = get_object_or_404(Usuarios, pk=pk)
    usuario.ativo = not usuario.ativo
    usuario.save()
    messages.success(request, 'Status alterado com sucesso!')
    return redirect('motoristas')

class Login_view(View):
    """
    View que exibe a tela de login e autentica o usuario
    """
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            usuario = authenticate(username=form.cleaned_data['login'], password=form.cleaned_data['senha'])
            if not usuario:
                messages.error(request, 'Login ou senha incorretos, verifique novamente!')
            elif not usuario.ativo:
                messages.error(request, 'Usuario desativado, fale com algum administrador!')
            else:
                login(request, usuario)
                return redirect('home')
        return redirect('login')


def logout_view(request):
    """
    Realiza o logout do usuario
    """
    logout(request)
    messages.success(request, 'Usuário desconectado com sucesso!')
    return redirect('login')
