from django import forms
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuarios
from django.urls import reverse_lazy

class UsuariosForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Usuario.
    """
    url = reverse_lazy('usuarios_cadastrar')
    _edit = False
    class Meta:
        model = Usuarios
        fields = ['username', 'password', 'cargo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'minlength':4, 'maxlength':12}),
            'cargo': forms.Select(attrs={'class': 'form-select form-select-sm h-100'})
        }
    
    def __init__(self, *args, **kwargs):
        """
        Personaliza as escolhas de campos choiceField.
        """
        if kwargs.get('instance'):
            self._password = kwargs['instance'].password
            self._edit = True
            kwargs['instance'].password = None
        super().__init__(*args, **kwargs)

        if self.instance != None:
            self.fields['password'].required = False

    def save(self, *args, **kwargs):
        senha_nova = self.cleaned_data['password']
        if self._edit:
            senha_antiga = self._password
            if not check_password(senha_nova, senha_antiga) and senha_nova != '':
                self.instance.password = make_password(senha_nova)
            else:
                self.instance.password = senha_antiga
        return super().save(*args, **kwargs)


class LoginForm(forms.Form):
    """
    Formulario de login
    """
    login = forms.CharField(label='Login:', max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    senha = forms.CharField(label='Senha:', max_length=12, min_length=4, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
