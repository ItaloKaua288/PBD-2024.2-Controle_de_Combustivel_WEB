# Generated by Django 5.1.3 on 2024-12-07 02:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0001_initial'),
        ('postos', '0002_alter_abastecimento_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='abastecimento',
            name='financeiro',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='abastecimentos', to='financeiro.financeiro'),
        ),
    ]
