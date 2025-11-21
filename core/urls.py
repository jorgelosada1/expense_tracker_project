from django.urls import path
from . import views
from .views import exportar_excel, cambiarcategoria

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('lista/', views.transaccion_lista, name='transaccion_lista'), 
    path('eliminar/<int:pk>/', views.eliminar_transaccion, name='eliminar_transaccion'), 
    path('editar/<int:pk>/', views.editar_transaccion, name='editar_transaccion'), 
    path("exportar-excel/", exportar_excel, name="exportar_excel"),
    path("cambiarcategoria/", cambiarcategoria, name="cambiarcategoria"), 
]
