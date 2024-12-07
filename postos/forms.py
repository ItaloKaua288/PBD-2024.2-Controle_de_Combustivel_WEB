from django import forms
from django.utils import timezone
from datetime import datetime
from veiculos.models import TipoCombustivel, Veiculo
from .validators import cnpj_validator
from .models import Posto, Abastecimento

def get_list_tipo_combustivel():
    queryset = TipoCombustivel.objects.all()
    return [(queryset.get(tipo=x[0]).pk, x[1]) for x in TipoCombustivel.tipos_choice] 

class PostoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Postos.
    """
    class Meta:
        model = Posto
        fields = ['nome', 'cnpj', 'tipos_combustivel']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'tipos_combustivel': forms.SelectMultiple(attrs={'class': 'form-select form-select-sm'})
        }
    
    def __init__(self, *args, **kwargs):
        """
        Personaliza as escolhas de campos choiceField e torna todos os campos obrigatórios.
        """
        super().__init__(*args, **kwargs)
        self.fields['tipos_combustivel'].choices = get_list_tipo_combustivel()

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        cnpj_validator(cnpj)
        return cnpj
    

class AbastecimentoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Abastecimentos.
    """
    class Meta:
        model = Abastecimento
        fields = ['posto', 'veiculo','tipo_combustivel', 'quilometragem', 'litros', 'valor_litro']
        widgets = {
            'posto': forms.Select(attrs={'class': 'form-select h-100'}),
            'veiculo': forms.Select(attrs={'class': 'form-select h-100'}),
            'quilometragem': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'tipo_combustivel': forms.Select(attrs={'class': 'form-select h-100'}),
            'litros': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'valor_litro': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        """
        Personaliza as escolhas de campos choiceField e torna todos os campos obrigatórios.
        """
        super().__init__(*args, **kwargs)
        self.fields['posto'].queryset = Posto.objects.filter(ativo=True)
        self.fields['veiculo'].queryset = Veiculo.objects.filter(ativo=True)
        self.fields['tipo_combustivel'].choices = get_list_tipo_combustivel()

    def clean_valor_positivo(self, value, campo_nome):
        if value <= 0:
            raise forms.ValidationError(f"O valor de {campo_nome} deve ser maior que zero.")
        return value
    
    def clean_litros(self):
        if self.cleaned_data['litros'] > self.cleaned_data['veiculo'].capacidade_tanque:
            raise forms.ValidationError(f'Quantidade de litros maior que a capacidade máxima do tanque!')
        return self.clean_valor_positivo(value=self.cleaned_data['litros'], campo_nome='litros')
    
    def clean_valor_litro(self):
        return self.clean_valor_positivo(value=self.cleaned_data['valor_litro'], campo_nome='"valor litro"')
    
    def clean_quilometragem(self):
        value = self.clean_valor_positivo(value=self.cleaned_data['quilometragem'], campo_nome='quilometragem')
        quilometragem_veiculo = self.cleaned_data['veiculo'].quilometragem
        if value < quilometragem_veiculo:
            raise forms.ValidationError(f'Quilometragem não pode ser menor que a anterior {quilometragem_veiculo}')
        return value
    
    def clean_tipo_combustivel(self):
        value = self.cleaned_data.get('tipo_combustivel')
        if not self.cleaned_data.get('veiculo').tipo_combustivel.filter(tipo=value).exists():
            raise forms.ValidationError('Esse veiculo não aceita esse tipo de combustivel.')
        return value

    def save(self, *args, **kwargs):
        self.cleaned_data['veiculo'].quilometragem = self.cleaned_data['quilometragem']
        self.cleaned_data['veiculo'].save()
        return super().save(*args, **kwargs)

class BuscaForm(forms.Form):
    """
    Formulario de busca por periodo
    """
    data_inicio = forms.DateField(label='Inicio', widget=forms.TextInput(
        attrs={'class': 'form-control datepicker periodo-datepicker', 'placeholder': 'Data início',}),
        required=True
    )
    data_fim = forms.DateField(label='Fim', widget=forms.TextInput(
        attrs={'class': 'form-control datepicker periodo-datepicker', 'placeholder': 'Data fim',}), 
        initial=datetime.strptime(str(timezone.now().date()), '%Y-%m-%d'),
        required=True
    )