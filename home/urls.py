from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view.as_view(), name='home'),
]
