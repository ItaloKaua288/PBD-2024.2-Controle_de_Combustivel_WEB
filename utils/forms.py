from django import forms
from django.utils import timezone
from datetime import datetime

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

def get_data_form(request):
    try: data_inicio = datetime.strptime(request.GET.get('data_inicio'), "%d-%m-%Y")
    except: data_inicio = None
    try: data_fim = datetime.strptime(request.GET.get('data_fim'), "%d-%m-%Y")
    except: data_fim = None
    return [data_inicio, data_fim]