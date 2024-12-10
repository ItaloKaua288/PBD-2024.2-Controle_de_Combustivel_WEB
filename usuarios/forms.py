from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuarios

class UsuariosForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Usuario.
    """
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
        if kwargs.get('instance'): self._password = kwargs['instance'].password
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            if self._password != self.cleaned_data['password']:
                self.instance.password = make_password(self.instance.password)
        except AttributeError:
            print(self.instance.password, 'fafsfas')
            self.instance.password = make_password(self.instance.password)
        return super().save(*args, **kwargs)


class LoginForm(forms.Form):
    """
    Formulario de login
    """
    login = forms.CharField(label='Login:', max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    senha = forms.CharField(label='Senha:', max_length=12, min_length=4, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
