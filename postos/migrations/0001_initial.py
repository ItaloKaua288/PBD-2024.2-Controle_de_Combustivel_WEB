# Generated by Django 5.1.3 on 2024-11-20 03:57

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import postos.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('veiculos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150, validators=[django.core.validators.MaxLengthValidator(limit_value=150)])),
                ('cnpj', models.CharField(max_length=18, unique=True, validators=[postos.validators.cnpj_validator])),
                ('tipos_combustivel', models.ManyToManyField(related_name='tipos_combustivel', to='veiculos.tipocombustivel')),
            ],
            options={
                'verbose_name': 'Posto',
                'verbose_name_plural': 'Postos',
            },
        ),
        migrations.CreateModel(
            name='Abastecimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('litros', models.FloatField(default=0)),
                ('valor_litro', models.FloatField(default=0, validators=[postos.validators.preco_validator])),
                ('valor_total', models.FloatField(default=0, validators=[postos.validators.preco_validator])),
                ('data_abastecimento', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_cadastrado', models.DateTimeField(default=django.utils.timezone.now)),
                ('tipo_combustivel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='veiculos.tipocombustivel')),
                ('veiculo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='veiculos.veiculo')),
                ('posto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='postos.posto')),
            ],
        ),
    ]
