from django.db import models
from .validators import cnpj_validator, preco_validator
from veiculos.models import TipoCombustivel, Veiculo
from financeiro.models import Financeiro

class Posto(models.Model):
    """
    Representa um posto de combustíveis.
    """
    nome = models.CharField(max_length=150, null=False, blank=False)
    cnpj = models.CharField(max_length=18, unique=True, null=False, blank=False, validators=[cnpj_validator])
    tipos_combustivel = models.ManyToManyField(TipoCombustivel, related_name='postos')
    ativo = models.BooleanField(default=True, null=False, blank=False)

    def __str__(self):
        return self.nome

class Abastecimento(models.Model):
    """
    Representa um abastecimento realizado em um posto para um veículo.
    """
    posto = models.ForeignKey(Posto, on_delete=models.SET_NULL, null=True, related_name='abastecimentos')
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True, related_name='abastecimentos')
    tipo_combustivel = models.ForeignKey(TipoCombustivel, on_delete=models.SET_NULL, null=True, related_name='abastecimentos')
    litros = models.FloatField(default=0, null=False, blank=False)
    valor_litro = models.FloatField(default=0, null=False, blank=False, validators=[preco_validator])
    valor_total = models.FloatField(default=0, editable=False)
    data_abastecimento = models.DateTimeField(auto_now_add=True)
    quilometragem = models.FloatField(default=0, null=False, blank=False)
    financeiro = models.ManyToManyField(Financeiro, related_name='abastecimentos')

    class Meta:
        ordering = ['-data_abastecimento']

    def __str__(self):
        return f'{self.posto}_{self.veiculo}_{self.data_abastecimento}'
    
    def save(self, *args, **kwargs):
        self.valor_total = self.litros * self.valor_litro
        super().save(*args, **kwargs)

