from django import forms
from .models import Transaccion, Categoria

class TransaccionForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all().order_by('nombre'),
        empty_label="Selecciona una Categoría",
        widget=forms.Select(attrs={'class': 'w-full p-2 border rounded-md'})
    )
    
    descripcion = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md', 'placeholder': 'Ej: Almuerzo, Salario, etc.'})
    )

    monto = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-md', 'placeholder': 'Ej: 50.00'})
    )
    
    class Meta:
        model = Transaccion
        fields = ['descripcion', 'monto', 'categoria']