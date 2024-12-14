# Generated by Django 5.1.3 on 2024-12-11 17:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0001_initial'),
        ('postos', '0004_remove_abastecimento_financeiro_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abastecimento',
            name='financeiro',
        ),
        migrations.AddField(
            model_name='abastecimento',
            name='financeiro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='abastecimentos', to='financeiro.financeiro'),
        ),
    ]
