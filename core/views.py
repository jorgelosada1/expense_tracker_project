from django.shortcuts import render
from django.db.models import Sum
from django.http import HttpResponse 
from .models import Transaccion, Categoria
from .forms import TransaccionForm
from django.http import HttpResponseNotAllowed, HttpResponse
import json
import random

def _get_finance_data():
    """Calcula el balance y recupera todas las transacciones."""
    transacciones = Transaccion.objects.select_related('categoria').all()
    
    balance_total = 0
    for t in transacciones:
        if t.categoria.es_ingreso:
            balance_total += t.monto
        else:
            balance_total -= t.monto
            
    balance_formateado = f"${balance_total:,.2f}"
    
    return transacciones, balance_formateado

def dashboard(request):

    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            response = HttpResponse(status=204)
            response['HX-Trigger'] = 'transaccionCreada'
            return response
    else:
        form = TransaccionForm()

    transacciones, balance_formateado = _get_finance_data()

    chart = _get_chart_data()

    context = {
        'titulo': 'Dashboard de Finanzas',
        'form': form,
        'transacciones': transacciones,
        'balance': balance_formateado,

        'chart_labels': chart["labels"],
        'chart_data': chart["data"],
        'chart_colors': chart["colors"],
    }

    return render(request, 'dashboard.html', context)


# -----------------------------------------------------------------------------------------

def transaccion_lista(request):
    transacciones, balance_formateado = _get_finance_data()

    chart = _get_chart_data()

    context = {
        'transacciones': transacciones,
        'balance': balance_formateado,
        'chart_labels': chart["labels"],
        'chart_data': chart["data"],
        'chart_colors': chart["colors"],
    }

    return render(request, 'transaccion_lista.html', context)


# --------------------------------------------------------------------------------------------

def eliminar_transaccion(request, pk):
    """
    Vista para eliminar una transacción específica (solo acepta DELETE de HTMX).
    """
    if request.method == 'DELETE':
        try:
            transaccion = Transaccion.objects.get(pk=pk)
            transaccion.delete()
            
            response = HttpResponse(status=204) 
            response['HX-Trigger'] = 'transaccionCreada' 
            return response
        except Transaccion.DoesNotExist:
            return HttpResponse(status=404)
    
    return HttpResponseNotAllowed(['DELETE'])

# -------------------------------------------------------------------------------------------

def editar_transaccion(request, pk):
    """
    Vista para cargar el formulario de edición (GET) y procesar la actualización (POST).
    Devuelve un fragmento HTML para ser cargado en un modal de HTMX.
    """
    try:
        transaccion = Transaccion.objects.get(pk=pk)
    except Transaccion.DoesNotExist:
        return HttpResponse(status=404)
        
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            form.save()
            
            response = HttpResponse(status=204)
            response['HX-Trigger'] = 'transaccionCreada, cerrarModal' 
            return response
    else:
        form = TransaccionForm(instance=transaccion)

    context = {
        'form': form,
        'transaccion': transaccion,
    }
    return render(request, 'editar_transaccion_form.html', context)



def _get_chart_data():
    categorias = Categoria.objects.all()

    labels = []
    data = []
    colors = []

    for cat in categorias:
        transacciones = Transaccion.objects.filter(categoria=cat)

        total = 0
        for t in transacciones:
            if t.categoria.es_ingreso:
                total += t.monto
            else:
                total += t.monto
        if total > 0:
            labels.append(cat.nombre)
            data.append(float(total))
            colors.append(f"#{random.randint(0, 0xFFFFFF):06x}")

    return {
        "labels": json.dumps(labels),
        "data": json.dumps(data),
        "colors": json.dumps(colors)
    }
