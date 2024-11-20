from django.db import models
from django.core.validators import MaxLengthValidator
from django.utils import timezone
from .validators import cnpj_validator, preco_validator
from veiculos.models import TipoCombustivel, Veiculo

class Posto(models.Model):
    nome = models.CharField(max_length=150, null=False, blank=False, validators=[MaxLengthValidator(limit_value=150)])
    cnpj = models.CharField(max_length=18, unique=True, null=False, blank=False, validators=[cnpj_validator])
    tipos_combustivel = models.ManyToManyField(TipoCombustivel, related_name='tipos_combustivel')
    ativo = models.BooleanField(default=True, null=False, blank=False)

    class Meta:
        verbose_name = ("Posto")
        verbose_name_plural = ("Postos")

    def __str__(self):
        return self.nome

class Abastecimento(models.Model):
    posto = models.ForeignKey(Posto, on_delete=models.SET_NULL, null=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True)
    tipo_combustivel = models.ForeignKey(TipoCombustivel, on_delete=models.SET_NULL, null=True)
    litros = models.FloatField(default=0, null=False, blank=False)
    valor_litro = models.FloatField(default=0, null=False, blank=False, validators=[preco_validator])
    valor_total = models.FloatField(default=0, null=False, blank=False, validators=[preco_validator])
    data_abastecimento = models.DateTimeField(default=timezone.now, null=False, blank=False)
    data_cadastrado = models.DateTimeField(default=timezone.now, null=False, blank=False)

    def __str__(self):
        return f'{self.posto}_{self.veiculo}_{self.data_cadastrado}'
