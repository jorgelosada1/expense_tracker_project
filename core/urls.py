from django.urls import path
from . import views 

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('lista/', views.transaccion_lista, name='transaccion_lista'), 
    path('eliminar/<int:pk>/', views.eliminar_transaccion, name='eliminar_transaccion'), 
    path('editar/<int:pk>/', views.editar_transaccion, name='editar_transaccion'), 
]