from django import forms
from veiculos.models import TipoCombustivel, Veiculo
from .validators import cnpj_validator
from .models import Posto
from django.utils import timezone


class PostoForm(forms.Form):
    combustivel_choices = [x for x in TipoCombustivel.tipos_choice]

    nome = forms.CharField(label='Nome:', max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cnpj = forms.CharField(label='CNPJ:', max_length=18, required=True, validators=[cnpj_validator], widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipos_combustivel = forms.MultipleChoiceField(label='Combustiveis:', choices=combustivel_choices, required=True, widget=forms.SelectMultiple(attrs={'class': 'form-select form-select-sm'}))

class AbastecimentoForm(forms.Form):
    posto_choices = [(x.pk, x.nome) for x in Posto.objects.all()]
    veiculo_choices = [(x.pk, f'{x.placa} - {x.modelo.nome}') for x in Veiculo.objects.all()]
    combustivel_choices = [x for x in TipoCombustivel.tipos_choice]

    posto = forms.ChoiceField(label='Posto:', choices=posto_choices, required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    veiculo = forms.ChoiceField(label='Veiculo:', choices=veiculo_choices, required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    tipo_combustivel = forms.ChoiceField(label='Tipo Combustivel:', choices=combustivel_choices, required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    litros = forms.FloatField(label='Litros:', required=True, initial=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'min':0}))
    valor_litro = forms.FloatField(label='Valor por litros R$:', required=True, initial=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'min':0}))
    data_abastecimento = forms.DateTimeField(label='Data:', required=True, initial=timezone.now, widget=forms.DateInput(attrs={'class':'form-control','type': 'datetime-local', 'max': timezone.now().strftime('%Y-%m-%dT00:00:00:00')}))
