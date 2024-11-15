from django.urls import path
from . import views

urlpatterns = [
    path('', views.usuariosView, name='usuarios'),
    path('auth/login/', views.loginView, name='login'),
    path('auth/logout/', views.logoutView, name='logout'),
]
