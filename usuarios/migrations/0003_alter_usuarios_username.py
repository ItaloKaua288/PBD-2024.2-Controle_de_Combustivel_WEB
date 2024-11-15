# Generated by Django 5.1.3 on 2024-11-15 17:17

import django.contrib.auth.validators
import usuarios.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_usuarios_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='username',
            field=models.CharField(error_messages={'unique': 'Usuario já existe'}, max_length=50, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator, usuarios.validators.username_validator]),
        ),
    ]
