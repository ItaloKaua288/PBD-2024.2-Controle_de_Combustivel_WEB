from django.urls import path
from . import views

urlpatterns = [
    path('', views.Postos_view.as_view(), name='postos'),
    path('cadastrar/', views.Posto_cadastrar_view.as_view(), name='postos_cadastrar'),
    path('editar/<int:pk>', views.Posto_editar_view.as_view(), name='postos_editar'),
    path('desativar/<int:pk>', views.postos_desativar_view, name='postos_desativar'),
    path('abastecimentos/', views.Abastecimento_listar_view.as_view(), name='abastecimentos'),
    path('abastecimentos/cadastrar/', views.Abastecimento_cadastrar_view.as_view(), name='abastecimentos_cadastrar'),
    path('abastecimentos/editar/<int:pk>', views.Abastecimento_editar_view.as_view(), name='abastecimentos_editar'),
    path('abastecimentos/vizualizar/<int:pk>/', views.Abastecimento_view.as_view(), name='abastecimentos_vizualizar'),

]
