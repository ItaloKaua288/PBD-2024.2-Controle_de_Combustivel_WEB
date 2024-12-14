from django import forms
from .models import TipoCombustivel, Modelo, Veiculo
from django.urls import reverse_lazy

class VeiculoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Veiculo.
    """
    url = reverse_lazy('veiculos_cadastrar')
    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo', 'capacidade_tanque', 'quilometragem', 'tipo_combustivel']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'minlength':8, 'placeholder':'XXX-XXXX'}),
            'modelo': forms.Select(attrs={'class': 'form-select form-select-sm p-2'}),
            'capacidade_tanque': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'quilometragem': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'tipo_combustivel': forms.SelectMultiple(attrs={'class': 'form-select form-select-sm'})
        }
    
    def __init__(self, *args, **kwargs):
        """
        Personaliza as escolhas de campos choiceField.
        """
        super().__init__(*args, **kwargs)
        self.fields['modelo'].choices = [(x.pk, x.nome) for x in Modelo.objects.all()]
        queryset = TipoCombustivel.objects.all()
        self.fields['tipo_combustivel'].choices = [(queryset.get(tipo=x[0]).pk, x[1]) for x in TipoCombustivel.tipos_choice]

    def save(self, *args, **kwargs):
        print(self.instance.quilometragem)
        return super().save(*args, **kwargs)

    def clean_capacidade_tanque(self):
        capacidade_tanque = self.cleaned_data.get('capacidade_tanque')
        if not isinstance(capacidade_tanque, float) or capacidade_tanque <= 0:
            raise forms.ValidationError('A capacidade do tanque deve ser maior que 0!')
        return capacidade_tanque
    
    def clean_quilometragem(self):
        quilometragem = self.cleaned_data.get('quilometragem')
        if not isinstance(quilometragem, float) or quilometragem < 0:
            raise forms.ValidationError('A quilometragem deve ser um número positivo!')
        return quilometragem