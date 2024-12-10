from veiculos.models import Veiculo, TipoCombustivel
from rolepermissions.mixins import HasRoleMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages

def abast_possui_financeiro(obj):
    return obj.financeiro.exists()

def possui_financeiro(obj):
        """
        Verifica se o objeto que possui uma lista de armazenamentos possui algum financeiro relacionado.
        """
        return obj.abastecimentos.prefetch_related('financeiro').filter(financeiro__isnull=False).exists()

def get_list_placa(queryset):
    lista = [Veiculo.objects.get(pk=x['veiculo']).placa for x in queryset]
    return lista

def get_list_combustivel(queryset):
    lista = {}
    for x in queryset:
        lista[f'{get_combustivel_tipo(TipoCombustivel.objects.get(pk=x['tipo_combustivel']).tipo)}'] = x['litros']
    return lista

def get_combustivel_tipo(value):
    tipos = TipoCombustivel.tipos_choice
    for x in tipos:
        if x[0] == value:
            return x[1]
        
class HasRoleMixinCustom(HasRoleMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            messages.error(request, 'Você não possui acesso a está área do sistema!')
            return redirect('home')
        
