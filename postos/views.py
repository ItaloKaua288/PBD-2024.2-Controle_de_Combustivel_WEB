from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from rolepermissions.decorators import has_role_decorator
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.roles import get_user_roles
from .models import Posto, Abastecimento
from .forms import PostoForm, AbastecimentoForm, BuscaForm
from utils.utils import get_perfil_logado
from datetime import datetime

class Postos_view(LoginRequiredMixin, HasRoleMixin, ListView):
    """
    Exibe a lista de postos, com suporte a busca.
    """
    model = Posto
    queryset = Posto.objects.all()
    template_name = 'postos.html'
    login_url = reverse_lazy('login')
    required_permission = 'Administrador'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_logado'] = get_perfil_logado(self.request)
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if get_user_roles(request.user)[0].__name__ == 'Administrador':
                return super().dispatch(request, *args, **kwargs)
            return redirect('usuarios_perfil', 1)
        return redirect('login')
    
    def get_queryset(self):
        return Posto.objects.filter(nome__icontains=self.request.GET.get('busca-input') if self.request.GET.get('busca-input') else '')

class Posto_cadastrar_view(LoginRequiredMixin, HasRoleMixin, CreateView):
    """
    View para cadastrar novos postos.
    """
    model = Posto
    form_class = PostoForm
    template_name = 'base_cadastrar.html'
    login_url = reverse_lazy('login')
    required_permission = 'Administrador'
    success_url = reverse_lazy('postos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_logado'] = get_perfil_logado(self.request)
        return context
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Posto adicionado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
class Posto_editar_view(LoginRequiredMixin, HasRoleMixin, UpdateView):
    """
    Edita as informações de um posto existente.
    """
    model = Posto
    form_class = PostoForm
    template_name = 'base_editar.html'
    login_url = reverse_lazy('login')
    required_permission = 'Administrador'
    success_url = reverse_lazy('postos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_logado'] = get_perfil_logado(self.request)
        return context
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Posto atualizado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def postos_desativar_view(request, pk):
    """
    Ativa ou desativa um posto existente.
    """
    posto = get_object_or_404(Posto, pk=pk)
    posto.ativo = not posto.ativo
    posto.save()
    messages.success(request, 'Status alterado com sucesso!')
    return redirect('postos')

class Abastecimento_view(LoginRequiredMixin, HasRoleMixin, ListView):
    """
    Exibe a lista de abastecimentos com suporte a filtros por data e páginas.
    """
    model = Abastecimento
    queryset = Abastecimento.objects.all()
    template_name = 'abastecimentos.html'
    login_url = reverse_lazy('login')
    required_permission = 'Administrador'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_logado'] = get_perfil_logado(self.request)
        context['busca_form'] = BuscaForm()
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if get_user_roles(request.user)[0].__name__ == 'Administrador':
                return super().dispatch(request, *args, **kwargs)
            return redirect('usuarios_perfil', 1)
        return redirect('login')

    def get_queryset(self):
        try: data_inicio = datetime.strptime(self.request.GET.get('data_inicio'), "%d-%m-%Y")
        except: data_inicio = None
        try: data_fim = datetime.strptime(self.request.GET.get('data_fim'), "%d-%m-%Y")
        except: data_fim = None

        if None not in [data_inicio, data_fim]:
            return Abastecimento.objects.filter(data_abastecimento__range=[data_inicio, data_fim])
        if data_inicio != None and data_fim == None:
            return Abastecimento.objects.filter(data_abastecimento__gte=data_inicio)
        if data_inicio == None and data_fim != None:
            return Abastecimento.objects.filter(data_abastecimento__lte=data_fim)
        return super().get_queryset()
    
    
class Abastecimento_cadastrar_view(LoginRequiredMixin, HasRoleMixin, CreateView):
    """
    Cadastra novos abastecimentos.
    """
    model = Abastecimento
    form_class = AbastecimentoForm
    template_name = 'base_cadastrar.html'
    login_url = reverse_lazy('login')
    required_permission = 'Administrador'
    success_url = reverse_lazy('abastecimentos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_logado'] = get_perfil_logado(self.request)
        return context
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Abastecimento adicionado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

class Abastecimento_editar_view(LoginRequiredMixin, HasRoleMixin, UpdateView):
    """
    Edita informações de um abastecimento existente.
    """
    model = Abastecimento
    form_class = AbastecimentoForm
    template_name = 'base_editar.html'
    login_url = reverse_lazy('login')
    required_permission = 'Administrador'
    success_url = reverse_lazy('abastecimentos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_logado'] = get_perfil_logado(self.request)
        return context
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Abastecimento atualizado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
