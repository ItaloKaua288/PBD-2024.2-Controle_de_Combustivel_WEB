from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from rolepermissions.decorators import has_role_decorator
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.roles import get_user_roles
from .models import Veiculo
from .forms import VeiculoForm
from utils.utils import get_perfil_logado

class Veiculos_view(LoginRequiredMixin, HasRoleMixin, ListView):
    """
    Mostra a lista de veiculos cadastrados.
    """
    model = Veiculo
    queryset = Veiculo.objects.all()
    template_name = 'veiculos.html'
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
        return Veiculo.objects.filter(placa__icontains=self.request.GET.get('busca-input') if self.request.GET.get('busca-input') else '')

class Veiculo_cadastrar_view(LoginRequiredMixin, HasRoleMixin, CreateView):
    """
    Cadastra novos veiculos.
    """
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'base_cadastrar.html'
    login_url = reverse_lazy('login')
    required_permission = 'Administrador'
    success_url = reverse_lazy('veiculos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_logado'] = get_perfil_logado(self.request)
        return context
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Veiculo adicionado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class Veiculo_editar_view(LoginRequiredMixin, HasRoleMixin, UpdateView):
    """
    Edita as informações de um posto existente.
    """
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'base_editar.html'
    login_url = reverse_lazy('login')
    required_permission = 'Administrador'
    success_url = reverse_lazy('veiculos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perfil_logado'] = get_perfil_logado(self.request)
        return context
    
    def form_valid(self, form):
        form.save()
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
