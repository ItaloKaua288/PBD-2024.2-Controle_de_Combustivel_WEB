from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    # path('postos/', include('postos.urls')),
    # path('abastecimentos/', include('abastecimentos.urls')),
    # path('home/', include('home.urls')),
    # path('veiculos/', include('veiculos.urls')),
    # path('relatorios/', include('relatorios.urls')),
]
