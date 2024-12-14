from django import forms
from django.utils import timezone
from veiculos.models import TipoCombustivel
from postos.models import Abastecimento
from .models import Financeiro
from django.db.models import Sum
import json
from django.urls import reverse_lazy

class FinanceiroAbastForm(forms.ModelForm):
    """
    Formulário do financeiro de abastecimento
    """
    url = reverse_lazy('financeiro_abast_cadastrar')
    class Meta:
        model = Financeiro
        fields = ['data_inicial', 'data_final']
        widgets = {
            'data_inicial': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'data_final': forms.DateInput(attrs={'class':'form-control','type':'date'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        data_inicial = cleaned_data.get('data_inicial')
        data_final = cleaned_data.get('data_final')
        
        if data_inicial and data_final and data_inicial > data_final:
            raise forms.ValidationError('A data inicial deve ser anterior à data final.')

        return cleaned_data

    def clean_data_final(self):
        self.abastecimentos = Abastecimento.objects.filter(
            data_abastecimento__date__range=[self.cleaned_data['data_inicial'], self.cleaned_data['data_final']],
            financeiro__isnull=True
        )

        if not self.abastecimentos.exists():
            raise forms.ValidationError('O sistema não possue abastecimentos disponiveis para geração de financeiro!')
        
        return self.cleaned_data['data_final']

    def _processar_abastecimentos(self):
        litros = {}
        totais = {}

        for tipo in self.abastecimentos.values('tipo_combustivel').annotate(litros_tot=Sum('litros'), valor_tot=Sum('valor_total')):
            cod_tipo = TipoCombustivel.objects.get(pk=tipo["tipo_combustivel"])
            litros[cod_tipo.tipo] = tipo['litros_tot']
            totais[cod_tipo.tipo] = tipo['valor_tot']

        return litros, totais,self.abastecimentos

    def save(self, *args, **kwargs):
        litros, totais, abastecimentos = self._processar_abastecimentos()
        self.instance.litros = json.dumps(litros)
        self.instance.totais = json.dumps(totais)
        instance = super().save(*args, **kwargs)

        for abast in abastecimentos:
            abast.financeiro = instance
            abast.save()

        return instance


class RelatorioVeiculoForm(forms.Form):
    """
    Formulario do filtro de por mês
    """
    mes_choices = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'), (5, 'Maio'), (6, 'Junho'), 
        (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
    ]
    mes = forms.ChoiceField(label='Mês', choices=mes_choices, initial=timezone.now().month,
                             widget=forms.Select(attrs={'class':'form-select'})
    )
    
