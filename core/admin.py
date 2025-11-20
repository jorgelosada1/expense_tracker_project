from django.contrib import admin
from .models import Categoria, Transaccion 

admin.site.register(Categoria)

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'monto', 'categoria', 'fecha') 
    
    list_filter = ('categoria', 'fecha') 
    
    search_fields = ('descripcion',)