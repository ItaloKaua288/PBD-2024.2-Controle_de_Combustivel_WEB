from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('veiculos/', include('veiculos.urls')),
    path('postos/', include('postos.urls')),
    path('financeiro/', include('financeiro.urls')),
]
