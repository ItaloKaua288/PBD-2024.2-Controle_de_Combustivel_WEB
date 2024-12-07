from django import forms
from django.utils import timezone
from veiculos.models import Veiculo

class RelatorioGeralForm(forms.Form):
    """
    Formulario do filtro de relatorio geral
    """
    mes_choices = ((1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), 
                   (4, 'Abril'), (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'), 
                   (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'))
    mes = forms.ChoiceField(label='Mês', choices=mes_choices, initial=timezone.now().month, 
                            widget=forms.Select(attrs={'class':'form-select'}))

class RelatorioVeiculoForm(RelatorioGeralForm):
    """
    Formulario do filtro de relatorio de veiculo
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['placa'] = forms.ModelChoiceField(label='Placa', queryset=Veiculo.objects.filter(ativo=True), 
                                   widget=forms.Select(attrs={'class':'form-select'}))