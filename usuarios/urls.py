from django.urls import path
from . import views

urlpatterns = [
    path('', views.Motoristas_view.as_view(), name='motoristas'),
    path('editar/<int:pk>/', views.Usuario_editar_view.as_view(), name='usuarios_editar'),
    path('desativar/<int:pk>/', views.usuarios_desativar_view, name='usuarios_desativar'),
    path('cadastrar/', views.Usuario_cadastrar_view.as_view(), name='usuarios_cadastrar'),
    path('auth/login/', views.Login_view.as_view(), name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
]
