from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.db.models import Q
from rolepermissions.decorators import has_role_decorator
from .models import Veiculo
from .forms import VeiculoForm
from utils.utils import HasRoleMixinCustom

class Veiculos_view(LoginRequiredMixin, HasRoleMixinCustom, ListView):
    """
    Mostra a lista de veiculos cadastrados.
    """
    model = Veiculo
    template_name = 'veiculos.html'
    login_url = reverse_lazy('login')
    paginate_by = 10
    allowed_roles = ['administrador']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cadastro_form'] = VeiculoForm()
        return context

    def get_queryset(self):
        """
        Retorna os veículos, filtrando por placa se a busca for fornecida.
        """
        busca = self.request.GET.get('busca', '')
        return Veiculo.objects.filter(Q(placa__icontains=busca) | Q(modelo__nome__icontains=busca) | Q(modelo__marca__nome__icontains=busca)).order_by('-id')

class Veiculo_cadastrar_view(LoginRequiredMixin, HasRoleMixinCustom, CreateView):
    """
    Cadastra novos veiculos no sistema.
    """
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'base_CRUD.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('veiculos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_titulo"] = 'Cadastrar'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Veiculo adicionado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

class Veiculo_editar_view(LoginRequiredMixin, HasRoleMixinCustom, UpdateView):
    """
    Edita as informações de um posto existente.
    """
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'base_CRUD.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('veiculos')
    allowed_roles = ['administrador']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_titulo"] = 'Editar'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Veiculo atualizado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def veiculos_desativar_view(request, pk):
    """
    Ativa ou desativa um posto existente.
    """
    veiculo = get_object_or_404(Veiculo, pk=pk)
    veiculo.ativo = not veiculo.ativo
    veiculo.save()
    messages.success(request, 'Status alterado com sucesso!')
    return redirect('veiculos')
