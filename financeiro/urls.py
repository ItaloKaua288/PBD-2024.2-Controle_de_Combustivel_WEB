from django.urls import path
from . import views

urlpatterns = [
    path('abastecimentos/', views.Financeiro_abast_listar_view.as_view(), name='financeiro_abast'),
    path('abastecimentos/cadastrar/', views.Financeiro_abast_cadastrar_view.as_view(), name="financeiro_abast_cadastrar"),
    path('abastecimentos/vizualizar/<int:pk>/', views.Financeiro_abast_view.as_view(), name='financeiro_abast_vizualizar'),
    path('abastecimentos/deletar/<int:pk>/', views.Financeiro_abast_deletar_view.as_view(), name='financeiro_abast_deletar'),
    # path('', views.geral_tmensal_view, name='relatorio_mensal'),
    path('relatorio/veiculo/<int:pk>', views.Relatorio_veiculo_view.as_view(), name='relatorio_veiculo'),
]
