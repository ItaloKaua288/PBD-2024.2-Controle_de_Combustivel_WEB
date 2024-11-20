from django import forms
from .models import Usuarios

class UsuariosForm(forms.Form):
    username = forms.CharField(label='Usuario:', max_length=50, min_length=4, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Senha:', max_length=12, min_length=4, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cargo = forms.ChoiceField(label='Cargo', choices=Usuarios.cargo_choices, required=True, initial='M', widget=forms.Select(attrs={'class': 'form-select'}))