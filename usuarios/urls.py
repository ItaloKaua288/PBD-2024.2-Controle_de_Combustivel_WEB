from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.loginView, name='login'),
]
