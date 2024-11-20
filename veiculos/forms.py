from django import forms
from .models import Marca, TipoCombustivel, Modelo

class VeiculoForm(forms.Form):
    marca_choices = [(x.pk, x.nome) for x in Marca.objects.all()]
    combustivel_choices = [x for x in TipoCombustivel.tipos_choice]
    modelo_choices = [(x.pk, x.nome) for x in Modelo.objects.all()]
    
    placa = forms.CharField(label='Placa:', max_length=8, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    modelo = forms.ChoiceField(label='Modelo:', choices=modelo_choices, required=True, widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    capacidade_tanque = forms.CharField(label='Capacidade Tanque:', initial=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'min':0}))
    combustivel = forms.MultipleChoiceField(label='Combustivel:', choices=combustivel_choices, required=True, widget=forms.SelectMultiple(attrs={'class': 'form-select form-select-sm'}))

class MarcaForm(forms.Form):
    nome = forms.CharField(label='Nome:', max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))