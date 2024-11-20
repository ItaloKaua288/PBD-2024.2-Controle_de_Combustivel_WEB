from django.db import models

class TipoCombustivel(models.Model):
    tipos_choice = (('G', 'Gasolina'), ('D', 'Diesel'), ('E', 'Etanol'))
    tipo = models.CharField(max_length=2, choices=tipos_choice, null=False, unique=True)

    def __str__(self):
        return self.tipo

class Marca(models.Model):
    nome = models.CharField(max_length=150, null=False, unique=True)

    def __str__(self):
        return self.nome

class Modelo(models.Model):
    nome = models.CharField(max_length=150, null=False, unique=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome
    
class Veiculo(models.Model):
    placa = models.CharField(max_length=8, null=False, unique=True)
    capacidade_tanque = models.FloatField(null=False, blank=False, default=0)
    ativo = models.BooleanField(default=True, null=False, blank=False)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    tipo_combustivel = models.ManyToManyField(TipoCombustivel, related_name='veiculos')

    def __str__(self):
        return self.placa