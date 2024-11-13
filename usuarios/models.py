from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from .userManagers import CustomUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save

class Usuarios(AbstractBaseUser, PermissionsMixin):
    cargo_choices = (('A', 'Admnistrador'), ('M', 'Motorista'))
    cargo = models.CharField(max_length=1, choices=cargo_choices, null=False, blank=False, default='M')
    username = models.CharField(max_length=150, unique=True, null=False, validators=[UnicodeUsernameValidator()], error_messages={'unique': 'Usuario já existe'})
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = ("usuario")
        verbose_name_plural = ("usuarios")

    @property
    def is_staff(self):
        return self.is_superuser
    objects = CustomUserManager()


# @receiver(post_save, sender=Usuarios)
# def create_token(sender, instance:Usuarios, created, **kwargs):
#     if created and instance.cargo == 'A':
#         token = TokenProxy(user=instance)
#         token.save()
# post_save.connect(create_token, sender=Usuarios)