from django.urls import path
from . import views

urlpatterns = [
    path('', views.postosView, name='postos'),
    path('cadastrar/', views.postosCadastrarView, name='postos_cadastrar'),
    path('editar/<int:pk>', views.postosEditarView, name='postos_editar'),
    path('desativar/<int:pk>', views.postosDesativarView, name='postos_desativar'),
    path('abastecimentos/', views.abastecimentosView, name='abastecimentos'),
    path('abastecimentos/cadastrar/', views.abastecimentosCadastrarView, name='abastecimentos_cadastrar'),
    path('abastecimentos/editar/<int:pk>', views.abastecimentosEditarView, name='abastecimentos_editar'),
]
