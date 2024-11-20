from django.urls import path
from . import views

urlpatterns = [
    path('', views.veiculosView, name='veiculos'),
    path('cadastrar/', views.veiculosCadastrarView, name='veiculos_cadastrar'),
    path('editar/<int:pk>', views.veiculosEditarView, name='veiculos_editar'),
    path('desativar/<int:pk>', views.veiculosDesativarView, name='veiculos_desativar'),
]
