from django.db import models

class Financeiro(models.Model):
    data_inicial = models.DateField(null=False, blank=False)
    data_final = models.DateField(null=False, blank=False)
    litros = models.TextField()
    totais = models.TextField()

    class Meta:
        ordering = ['-data_final']

    def __str__(self):
        return f'{self.data_inicial} - {self.data_final}'