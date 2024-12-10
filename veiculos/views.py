from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from rolepermissions.decorators import has_role_decorator
from .models import Veiculo
from .forms import VeiculoForm
from utils.utils import HasRoleMixinCustom, possui_financeiro


class Veiculos_view(LoginRequiredMixin, HasRoleMixinCustom, ListView):
    """
    Mostra a lista de veiculos cadastrados.
    """
    model = Veiculo
    template_name = 'veiculos.html'
    login_url = reverse_lazy('login')
    paginate_by = 10
    allowed_roles = ['administrador']

    def get_queryset(self):
        """
        Retorna os veículos, filtrando por placa se a busca for fornecida.
        """
        return Veiculo.objects.filter(placa__icontains=self.request.GET.get('busca-input', ''))

class Veiculo_cadastrar_view(LoginRequiredMixin, HasRoleMixinCustom, CreateView):
    """
    Cadastra novos veiculos no sistema.
    """
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'base_cadastrar.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('veiculos')
    
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
    template_name = 'base_editar.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('veiculos')
    allowed_roles = ['administrador']

    def dispatch(self, request, *args, **kwargs):
        if possui_financeiro(self.get_object()):
            messages.error(request, 'Veículo vinculado a financeiro, não pode ser editado.')
            return redirect('veiculos')
        return super().dispatch(request, *args, **kwargs)
    
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
