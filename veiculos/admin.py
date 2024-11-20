from django.contrib import admin
from .models import Marca, Veiculo, TipoCombustivel, Modelo

admin.site.register(Marca)
admin.site.register(Veiculo)
admin.site.register(TipoCombustivel)
admin.site.register(Modelo)