from django import forms
from django.utils import timezone
from veiculos.models import Veiculo, TipoCombustivel
from postos.models import Abastecimento
from .models import Financeiro
from django.db.models import Sum
import json

class FinanceiroAbastForm(forms.ModelForm):
    """
    Formulário do financeiro de abastecimento
    """
    class Meta:
        model = Financeiro
        fields = ['data_inicial', 'data_final']
        widgets = {
            'data_inicial': forms.DateInput(attrs={'class':'','type':'date'}),
            'data_final': forms.DateInput(attrs={'class':'','type':'date'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        data_inicial = cleaned_data.get('data_inicial')
        data_final = cleaned_data.get('data_final')

        if data_inicial and data_final and data_inicial > data_final:
            raise forms.ValidationError('A data inicial deve ser anterior à data final.')

        return cleaned_data

    def _processar_abastecimentos(self):
        abastecimentos = Abastecimento.objects.filter(data_abastecimento__date__range=[
            self.cleaned_data['data_inicial'], self.cleaned_data['data_final']
        ])
        litros = {}
        totais = {}

        for tipo in abastecimentos.values('tipo_combustivel').annotate(litros_tot=Sum('litros'), valor_tot=Sum('valor_total')):
            cod_tipo = TipoCombustivel.objects.get(pk=tipo["tipo_combustivel"])
            litros[cod_tipo.tipo] = tipo['litros_tot']
            totais[cod_tipo.tipo] = tipo['valor_tot']

        return litros, totais, abastecimentos

    def save(self, *args, **kwargs):
        litros, totais, abastecimentos = self._processar_abastecimentos()
        self.instance.litros = json.dumps(litros)
        self.instance.totais = json.dumps(totais)

        instance = super().save(*args, **kwargs)

        for abast in abastecimentos:
            abast.financeiro.add(instance)

        return instance

class RelatorioGeralForm(forms.Form):
    """
    Formulario do filtro de relatorio geral
    """
    mes_choices = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'), (5, 'Maio'), (6, 'Junho'), 
        (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
    ]
    mes = forms.ChoiceField(label='Mês', choices=mes_choices, initial=timezone.now().month, widget=forms.Select(attrs={'class':'form-select'}))

class RelatorioVeiculoForm(RelatorioGeralForm):
    """
    Formulario do filtro de relatorio de veiculo
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['placa'] = forms.ModelChoiceField(label='Placa', queryset=Veiculo.objects.filter(ativo=True), widget=forms.Select(attrs={'class':'form-select'}))
        