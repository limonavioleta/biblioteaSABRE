from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.index_clientes, name='index'),
    path('login/', views.login_cliente, name='login'),
    path('talleres/', views.inscribir_taller, name='inscribir_taller'),
]