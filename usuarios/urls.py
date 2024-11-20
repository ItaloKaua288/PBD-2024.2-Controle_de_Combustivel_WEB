from django.urls import path
from . import views

urlpatterns = [
    path('', views.usuariosView, name='usuarios'),
    path('perfil/<int:pk>/', views.usuariosPerfil, name='usuarios_perfil'),
    path('editar/<int:pk>/', views.usuariosEditarView, name='usuarios_editar'),
    path('desativar/<int:pk>/', views.usuariosDesativarView, name='usuarios_desativar'),
    path('deletar/<int:pk>/', views.usuariosDeletarView, name='usuarios_deletar'),
    path('cadastro/', views.usuariosCadastroView, name='usuarios_cadastro'),
    path('auth/login/', views.loginView, name='login'),
    path('auth/logout/', views.logoutView, name='logout'),
]
