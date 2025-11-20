from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    
    es_ingreso = models.BooleanField(default=False) 

    class Meta:
        verbose_name_plural = "Categorias" 

    def __str__(self):
        return self.nombre


class Transaccion(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=200)
    fecha = models.DateField(auto_now_add=True) 

    class Meta:
        ordering = ['-fecha'] 

    def __str__(self):
        tipo = "Ingreso" if self.categoria.es_ingreso else "Gasto"
        return f"[{tipo}] ${self.monto} - {self.descripcion}"