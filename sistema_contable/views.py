from django.shortcuts import render
from django.http import HttpResponse
from .models import Transaccion, ClaseCuenta, Cuenta
from .forms import TransaccionForm
from django.http import JsonResponse


# Create your views here.
def inicio(request):
    return render(request, 'transacciones/index.html')

def registroTransaccion(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            # Puedes redirigir a una página de confirmación o hacer lo que necesites
            #redirect('transacciones/registro_transaccion.html')
    else:
        form = TransaccionForm()

    # Cargar opciones de clases de cuentas y cuentas desde la base de datos
    clases_de_cuentas = ClaseCuenta.objects.all()
    cuentas = Cuenta.objects.all()

    return render(request, 'transacciones/registro_transaccion.html', {'form': form, 'clases_de_cuentas': clases_de_cuentas, 'cuentas': cuentas})




def catalogoCuentas(request):
    return render(request, 'transacciones/catalogo_cuentas.html')


def manoObra(request):
    return render(request, 'transacciones/mano_obra.html')    

def costos(request):
    return render(request, 'transacciones/costos.html')    

def balanzaComprobacion(request):
    transacciones = Transaccion.objects.all() #para tener todas las transacciones

    cuentas = Cuenta.objects.all()
    balance = []

    for cuenta in cuentas:
       # Excluye las cuentas de IVA Débito Fiscal y Crédito Fiscal
        if cuenta.nombre not in ["Iva debito fiscal", "Iva credito fiscal"]:

            transacciones_debe = Transaccion.objects.filter(cargo_cuenta=cuenta)
            transacciones_haber = Transaccion.objects.filter(abono_cuenta=cuenta)

            total_debe = sum(transaccion.monto for transaccion in transacciones_debe)
            total_haber = sum(transaccion.monto for transaccion in transacciones_haber)

            balance.append({
                'codigo_cuenta': cuenta.codigoCA,  # campo personalizado
                'nombre_cuenta': cuenta.nombre,
                'total_debe': total_debe,
                'total_haber': total_haber,
            })

    total_general_debe = sum(cuenta['total_debe'] for cuenta in balance)
    total_general_haber = sum(cuenta['total_haber'] for cuenta in balance)

    return render(request, 'transacciones/balanza_comprobacion.html', {
        'transacciones': transacciones,
        'balance': balance,
        'total_general_debe': total_general_debe,
        'total_general_haber': total_general_haber,
    })


def hojaTrabajo(request):
    return render(request, 'transacciones/hoja_trabajo.html')    

def cierraContable(request):
    return render(request, 'transacciones/cierre_contable.html')    


