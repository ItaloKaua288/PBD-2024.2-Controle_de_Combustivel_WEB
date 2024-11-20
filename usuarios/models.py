from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from .userManagers import CustomUserManager
from django.db.models.signals import post_save
from rolepermissions.roles import assign_role

class Usuarios(AbstractBaseUser, PermissionsMixin):
    cargo_choices = (('A', 'Admnistrador'), ('M', 'Motorista'))
    cargo = models.CharField(max_length=1, choices=cargo_choices, null=False, blank=False, default='M')
    username = models.CharField(max_length=50, unique=True, null=False, 
                                validators=[UnicodeUsernameValidator, MaxLengthValidator(limit_value=50), MinLengthValidator(limit_value=4)], 
                                error_messages={'unique': 'Usuario já existe'})
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = ("usuario")
        verbose_name_plural = ("usuarios")

    @property
    def is_staff(self):
        return self.is_superuser
    objects = CustomUserManager()

    def set_password(self, raw_password):
        if len(raw_password) > 12 or len(raw_password) < 4:
            raise ValidationError('Senha deve ser de 4 a 12 caracteres')
        self.password = make_password(raw_password)
        self._password = raw_password

def criar_usuario(sender, instance:Usuarios, created, **kwargs):
    if created:
        if instance.cargo == 'A':
            assign_role(instance, 'administrador')
        elif instance.cargo == 'M':
            assign_role(instance, 'motorista')
post_save.connect(criar_usuario, Usuarios)