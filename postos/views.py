from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from rolepermissions.decorators import has_role_decorator
from .models import Posto, Abastecimento
from .forms import PostoForm, AbastecimentoForm
from utils.utils import HasRoleMixinCustom
from utils.forms import BuscaForm, get_data_form

class Postos_view(LoginRequiredMixin, HasRoleMixinCustom, ListView):
    """
    Exibe a lista de postos, com suporte a busca.
    """
    model = Posto
    template_name = 'postos.html'
    login_url = reverse_lazy('login')
    paginate_by = 10
    allowed_roles = ['administrador']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cadastro_form'] = PostoForm()
        return context
    
    def get_queryset(self):
        busca = self.request.GET.get('busca', '')
        return Posto.objects.filter(Q(nome__icontains=busca) | Q(cnpj=busca))
 
class Posto_cadastrar_view(LoginRequiredMixin, HasRoleMixinCustom, CreateView):
    """
    View para cadastrar novos postos.
    """
    model = Posto
    form_class = PostoForm
    template_name = 'base_CRUD.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('postos')
    allowed_roles = ['administrador']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_titulo"] = 'Cadastrar'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Posto adicionado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
class Posto_editar_view(LoginRequiredMixin, HasRoleMixinCustom, UpdateView):
    """
    Edita as informações de um posto existente.
    """
    model = Posto
    form_class = PostoForm
    template_name = 'base_CRUD.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('postos')
    allowed_roles = ['administrador']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_titulo"] = 'Editar'
        return context
    
    def form_valid(self, form):
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

class Abastecimento_listar_view(LoginRequiredMixin, HasRoleMixinCustom, ListView):
    """
    Exibe a lista de abastecimentos com suporte a filtros por data e páginas.
    """
    model = Abastecimento
    template_name = 'abastecimentos.html'
    login_url = reverse_lazy('login')
    paginate_by = 10
    allowed_roles = ['administrador']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['busca_form'] = BuscaForm()
        context['cadastro_form'] = AbastecimentoForm()
        return context

    def get_queryset(self):
        datas = get_data_form(self.request)
        if None not in datas:
            return Abastecimento.objects.filter(data_abastecimento__date__range=datas)
        if datas[0]:
            return Abastecimento.objects.filter(data_abastecimento__date__gte=datas[0])
        if datas[1]:
            return Abastecimento.objects.filter(data_abastecimento__date__lte=datas[1])
        return super().get_queryset()
    
class Abastecimento_cadastrar_view(LoginRequiredMixin, HasRoleMixinCustom, CreateView):
    """
    Cadastra novos abastecimentos.
    """
    model = Abastecimento
    form_class = AbastecimentoForm
    template_name = 'base_CRUD.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('abastecimentos')
    allowed_roles = ['administrador']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_titulo"] = 'Cadastrar'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Abastecimento adicionado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

class Abastecimento_editar_view(LoginRequiredMixin, HasRoleMixinCustom, UpdateView):
    """
    Edita informações de um abastecimento existente caso não tenha financeiros gerados.
    """
    model = Abastecimento
    form_class = AbastecimentoForm
    template_name = 'base_CRUD.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('abastecimentos')
    allowed_roles = ['administrador']
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().financeiro:
            messages.error(request, 'Abastecimento vínculado a um financeiro, não é possivel editar!')
            return redirect('abastecimentos')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_titulo"] = 'Editar'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Abastecimento atualizado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    
class Abastecimento_view(LoginRequiredMixin, HasRoleMixinCustom, DetailView):
    """
    Exibe as informações de um abastecimento existente
    """
    model = Abastecimento
    template_name = 'abastecimentos_vizualizar.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('abastecimentos')
    allowed_roles = ['administrador']