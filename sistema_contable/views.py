from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def inicio(request):
    return render(request, 'transacciones/index.html')

def registroTransaccion(request):
    return render(request, 'transacciones/registro_transaccion.html')    

#Braian
def catalogoCuentas(request):

    cuentas = Cuenta_Cuenta.objects.all()
    
    diccionario_cuentas = {'cuentas': cuentas}

    return render(request, 'transacciones/catalogo_cuentas.html', diccionario_cuentas)


def manoObra(request):
    return render(request, 'transacciones/mano_obra.html')    

def costos(request):
    return render(request, 'transacciones/costos.html')    

def balanzaComprobacion(request):
    return render(request, 'transacciones/balanza_comprobacion.html')    

def hojaTrabajo(request):
    return render(request, 'transacciones/hoja_trabajo.html')    

def cierraContable(request):
    return render(request, 'transacciones/cierre_contable.html')    