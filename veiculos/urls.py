from django.urls import path
from . import views

urlpatterns = [
    path('', views.Veiculos_view.as_view(), name='veiculos'),
    path('cadastrar/', views.Veiculo_cadastrar_view.as_view(), name='veiculos_cadastrar'),
    path('editar/<int:pk>', views.Veiculo_editar_view.as_view(), name='veiculos_editar'),
    path('desativar/<int:pk>', views.veiculos_desativar_view, name='veiculos_desativar'),
]
