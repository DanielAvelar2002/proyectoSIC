from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import TransaccionForm
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.
def inicio(request):
    capital = Cuenta.objects.get(codigoCA  = 3101) #modificar
    utilidad = Cuenta.objects.get(codigoCA = 3101)
    venta = Cuenta.objects.get(codigoCA = 3101)
    ventasp=venta.saldo 
    total = (capital.saldo+utilidad.saldo) * (-1)
    return render(request, 'transacciones/index.html',{"total":total,"venta":ventasp})

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
     # Obtén todas las cuentas ordenadas por el campo 'codigoCA'
    cuentas = Cuenta.objects.all().order_by('codigoCA')

    return render(request, 'transacciones/catalogo_cuentas.html', {'cuentas': cuentas})


def manoObra(request):
    return render(request, 'transacciones/mano_obra.html')    

def costos(request):
    return render(request, 'transacciones/costos.html')    

def ingresarOrden(request):
    try:
        cantidadP = Decimal(request.POST['txtCantidad'])
        materiaDirecta = Decimal(request.POST['txtUno'])
        manoObraDirecta = Decimal(request.POST['txtDos'])
        costoIndirecto = Decimal(request.POST['txtTres'])
        ventas = Decimal(request.POST['txtCinco'])

        materiaDirecta = materiaDirecta*cantidadP
        manoObraDirecta = manoObraDirecta*cantidadP
        costoIndirecto = costoIndirecto*cantidadP
        costo = manoObraDirecta + materiaDirecta + costoIndirecto 
        
        objetoMD = Cuenta.objects.get(codigoCA = 4101)
        objetoMD.saldo = objetoMD.saldo + costo
        objetoMD.save()

        objetoCaja = Cuenta.objects.get(codigoCA =1101)
        objetoCaja.saldo = objetoCaja.saldo - costo
        objetoCaja.save()

        objetoVenta = Cuenta.objects.get(codigoCA = 5101)
        objetoVenta.saldo = objetoVenta.saldo - (ventas *cantidadP)
        objetoVenta.save()

        objetoCaja = Cuenta.objects.get(codigoCA =1101)
        objetoCaja.saldo = objetoCaja.saldo + (ventas *cantidadP)
        objetoCaja.save()

          
        messages.success(request,'¡Orden de fabricación registrada con éxito!')
    except Exception as e:
        messages.error(request,e)
        

    return redirect('/costos')
    
def balanzaComprobacion(request):
    transacciones = Transaccion.objects.all() #para tener todas las transacciones

    cuentas = Cuenta.objects.all()
    balance = []

    # -------------LOGICA PARA EL BALANCE DE COMPROBACION------------------ # 
    #Activos
    #Activos corrientes
    #Efectivo
    print("\nefectivo: ")
    cuenta_efectivo = Cuenta.objects.get(nombre="Efectivo")

    if cuenta_efectivo.saldo>0 and cuenta_efectivo.clase.nombre == "Activo":
        debe_efectivo=abs(cuenta_efectivo.saldo)
        haber_efectivo=0
        print("DEBE: ", debe_efectivo)
        print("HABER: ", haber_efectivo)
    elif cuenta_efectivo.saldo<0 and cuenta_efectivo.clase.nombre == "Activo":
        debe_efectivo=0
        haber_efectivo=abs(cuenta_efectivo.saldo)
        print("DEBE: ", debe_efectivo)
        print("HABER: ", haber_efectivo)
    else:
        debe_efectivo=0
        haber_efectivo=0
        print("DEBE: ", debe_efectivo)
        print("HABER: ", haber_efectivo)

    #Bancos
    print("\nbancos: ")
    cuenta_bancos = Cuenta.objects.get(nombre="Bancos")

    if cuenta_bancos.saldo>0 and cuenta_bancos.clase.nombre == "Activo":
        debe_bancos=abs(cuenta_bancos.saldo)
        haber_bancos=0
        print("DEBE: ", debe_bancos)
        print("HABER: ", haber_bancos)
    elif cuenta_bancos.saldo<0 and cuenta_bancos.clase.nombre == "Activo":
        debe_bancos=0
        haber_bancos=abs(cuenta_bancos.saldo)
        print("DEBE: ", debe_bancos)
        print("HABER: ", haber_bancos)
    else:
        debe_bancos=0
        haber_bancos=0
        print("DEBE: ", debe_bancos)
        print("HABER: ", haber_bancos)

    #Cuentas por cobrar
    print("\nCuentas por cobrar: ")
    cuenta_cuentasporcobrar = Cuenta.objects.get(nombre="Cuentas por cobrar")

    if cuenta_cuentasporcobrar.saldo>0 and cuenta_cuentasporcobrar.clase.nombre == "Activo":
        debe_cuentasporcobrar=abs(cuenta_cuentasporcobrar.saldo)
        haber_cuentasporcobrar=0
        print("DEBE: ", debe_cuentasporcobrar)
        print("HABER: ", haber_cuentasporcobrar)
    elif cuenta_cuentasporcobrar.saldo<0 and cuenta_cuentasporcobrar.clase.nombre == "Activo":
        debe_cuentasporcobrar=0
        haber_cuentasporcobrar=abs(cuenta_cuentasporcobrar.saldo)
        print("DEBE: ", debe_cuentasporcobrar)
        print("HABER: ", haber_cuentasporcobrar)
    else:
        debe_cuentasporcobrar=0
        haber_cuentasporcobrar=0
        print("DEBE: ", debe_cuentasporcobrar)
        print("HABER: ", haber_cuentasporcobrar)

    #Documentos por cobrar
    cuenta_documentosporcobrar = Cuenta.objects.get(nombre="Documentos por cobrar")
    print("\nDocumentos por cobrar")

    if cuenta_documentosporcobrar.saldo>0 and cuenta_documentosporcobrar.clase.nombre == "Activo":
        debe_documentosporcobrar=abs(cuenta_documentosporcobrar.saldo)
        haber_documentosporcobrar=0
        print("DEBE: ", debe_documentosporcobrar)
        print("HABER: ", haber_documentosporcobrar)
    elif cuenta_documentosporcobrar.saldo<0 and cuenta_documentosporcobrar.clase.nombre == "Activo":
        debe_documentosporcobrar=0
        haber_documentosporcobrar=abs(cuenta_documentosporcobrar.saldo)
        print("DEBE: ", debe_documentosporcobrar)
        print("HABER: ", haber_documentosporcobrar)
    else:
        debe_documentosporcobrar=0
        haber_documentosporcobrar=0
        print("DEBE: ", debe_documentosporcobrar)
        print("HABER: ", haber_documentosporcobrar)

    #Intereses por cobrar
    cuenta_interesesporcobrar = Cuenta.objects.get(nombre="Intereses por cobrar")
    print("\nIntereses por cobrar")

    if cuenta_interesesporcobrar.saldo>0 and cuenta_interesesporcobrar.clase.nombre == "Activo":
        debe_interesesporcobrar=abs(cuenta_interesesporcobrar.saldo)
        haber_interesesporcobrar=0
        print("DEBE: ", debe_interesesporcobrar)
        print("HABER: ", haber_interesesporcobrar)
    elif cuenta_interesesporcobrar.saldo<0 and cuenta_interesesporcobrar.clase.nombre == "Activo":
        debe_interesesporcobrar=0
        haber_interesesporcobrar=abs(cuenta_interesesporcobrar.saldo)
        print("DEBE: ", debe_interesesporcobrar)
        print("HABER: ", haber_interesesporcobrar)
    else:
        debe_interesesporcobrar=0
        haber_interesesporcobrar=0
        print("DEBE: ", debe_interesesporcobrar)
        print("HABER: ", haber_interesesporcobrar)
   
    #Gastos pagados por adelantado
    cuenta_gastospagadosporadelantado = Cuenta.objects.get(nombre="Gastos pagados por adelantado")
    print("\nGastos pagados por adelantado")

    if cuenta_gastospagadosporadelantado.saldo>0 and cuenta_gastospagadosporadelantado.clase.nombre == "Activo":
        debe_gastospagadosporadelantado=abs(cuenta_gastospagadosporadelantado.saldo)
        haber_gastospagadosporadelantado=0
        print("DEBE: ", debe_gastospagadosporadelantado)
        print("HABER: ", haber_gastospagadosporadelantado)
    elif cuenta_gastospagadosporadelantado.saldo<0 and cuenta_gastospagadosporadelantado.clase.nombre == "Activo":
        debe_gastospagadosporadelantado=0
        haber_gastospagadosporadelantado=abs(cuenta_gastospagadosporadelantado.saldo)
        print("DEBE: ", debe_gastospagadosporadelantado)
        print("HABER: ", haber_gastospagadosporadelantado)
    else:
        debe_gastospagadosporadelantado=0
        haber_gastospagadosporadelantado=0
        print("DEBE: ", debe_gastospagadosporadelantado)
        print("HABER: ", haber_gastospagadosporadelantado)

    #Papeleria y utiles
    cuenta_papeleriayutiles = Cuenta.objects.get(nombre="Papelería y útiles")
    print("\nPapeleria y utiles")

    if cuenta_papeleriayutiles.saldo>0 and cuenta_papeleriayutiles.clase.nombre == "Activo":
        debe_papeleriayutiles=abs(cuenta_papeleriayutiles.saldo)
        haber_papeleriayutiles=0
        print("DEBE: ", debe_papeleriayutiles)
        print("HABER: ", haber_papeleriayutiles)
    elif cuenta_papeleriayutiles.saldo<0 and cuenta_papeleriayutiles.clase.nombre == "Activo":
        debe_papeleriayutiles=0
        haber_papeleriayutiles=abs(cuenta_papeleriayutiles.saldo)
        print("DEBE: ", debe_papeleriayutiles)
        print("HABER: ", haber_papeleriayutiles)
    else:
        debe_papeleriayutiles=0
        haber_papeleriayutiles=0
        print("DEBE: ", debe_papeleriayutiles)
        print("HABER: ", haber_papeleriayutiles)

    #Iva credito fiscal
    print("\nIva credito fiscal")
    cuenta_ivacreditofiscal = Cuenta.objects.get(nombre="Iva credito fiscal")

    if cuenta_ivacreditofiscal.saldo>0 and cuenta_ivacreditofiscal.clase.nombre == "Activo":
        debe_ivacreditofiscal=abs(cuenta_ivacreditofiscal.saldo)
        haber_ivacreditofiscal=0
        print("DEBE: ", debe_ivacreditofiscal)
        print("HABER: ", haber_ivacreditofiscal)
    elif cuenta_ivacreditofiscal.saldo<0 and cuenta_ivacreditofiscal.clase.nombre == "Activo":
        debe_ivacreditofiscal=0
        haber_ivacreditofiscal=abs(cuenta_ivacreditofiscal.saldo)
        print("DEBE: ", debe_ivacreditofiscal)
        print("HABER: ", haber_ivacreditofiscal)
    else:
        debe_ivacreditofiscal=0
        haber_ivacreditofiscal=0
        print("DEBE: ", debe_ivacreditofiscal)
        print("HABER: ", haber_ivacreditofiscal)

    #Iva pagado por anticipado
    print("\nIva pagado por anticipado")
    cuenta_ivapagadoporanticipado = Cuenta.objects.get(nombre="IVA pagado por anticipado")

    if cuenta_ivapagadoporanticipado.saldo>0 and cuenta_ivapagadoporanticipado.clase.nombre == "Activo":
        debe_ivapagadoporanticipado=abs(cuenta_ivapagadoporanticipado.saldo)
        haber_ivapagadoporanticipado=0
        print("DEBE: ", debe_ivapagadoporanticipado)
        print("HABER: ", haber_ivapagadoporanticipado)
    elif cuenta_ivapagadoporanticipado.saldo<0 and cuenta_ivapagadoporanticipado.clase.nombre == "Activo":
        debe_ivapagadoporanticipado=0
        haber_ivapagadoporanticipado=abs(cuenta_ivapagadoporanticipado.saldo)
        print("DEBE: ", debe_ivapagadoporanticipado)
        print("HABER: ", haber_ivapagadoporanticipado)
    else:
        debe_ivapagadoporanticipado=0
        haber_ivapagadoporanticipado=0
        print("DEBE: ", debe_ivapagadoporanticipado)
        print("HABER: ", haber_ivapagadoporanticipado)

    #No corrientes
    #Insumos
    print("\nInsumos: ")
    cuenta_insumos = Cuenta.objects.get(nombre="Insumos")
    
    if cuenta_insumos.saldo>0 and cuenta_insumos.clase.nombre == "Activo":
        debe_insumos=abs(cuenta_insumos.saldo)
        haber_insumos=0
        print("DEBE: ", debe_insumos)
        print("HABER: ", haber_insumos)
    elif cuenta_insumos.saldo<0 and cuenta_insumos.clase.nombre == "Activo":
        debe_insumos=0
        haber_insumos=abs(cuenta_insumos.saldo)
        print("DEBE: ", debe_insumos)
        print("HABER: ", haber_insumos)
    else:
        debe_insumos=0
        haber_insumos=0
        print("DEBE: ", debe_insumos)
        print("HABER: ", haber_insumos)

    #Equipo informatico
    print("\nEquipo informatico: ")
    cuenta_equipoinformatico = Cuenta.objects.get(nombre="Equipo Informatico")
    
    if cuenta_equipoinformatico.saldo>0 and cuenta_equipoinformatico.clase.nombre == "Activo":
        debe_equipoinformatico=abs(cuenta_equipoinformatico.saldo)
        haber_equipoinformatico=0
        print("DEBE: ", debe_equipoinformatico)
        print("HABER: ", haber_equipoinformatico)
    elif cuenta_equipoinformatico.saldo<0 and cuenta_equipoinformatico.clase.nombre == "Activo":
        debe_equipoinformatico=0
        haber_equipoinformatico=abs(cuenta_equipoinformatico.saldo)
        print("DEBE: ", debe_equipoinformatico)
        print("HABER: ", haber_equipoinformatico)
    else:
        debe_equipoinformatico=0
        haber_equipoinformatico=0
        print("DEBE: ", debe_equipoinformatico)
        print("HABER: ", haber_equipoinformatico)

    #Pasivo
    #Corriente
    #Cuentas por pagar
    print("\nCuentas por pagar: ")
    cuenta_cuentasporpagar = Cuenta.objects.get(nombre="Cuentas por pagar")  

    if cuenta_cuentasporpagar.saldo<0 and cuenta_cuentasporpagar.clase.nombre == "Pasivo":
        debe_cuentasporpagar=0
        haber_cuentasporpagar=abs(cuenta_cuentasporpagar.saldo)        
        print("DEBE: ", debe_cuentasporpagar)
        print("HABER: ", haber_cuentasporpagar)
    elif cuenta_cuentasporpagar.saldo>0 and cuenta_cuentasporpagar.clase.nombre == "Pasivo":
        debe_cuentasporpagar=abs(cuenta_cuentasporpagar.saldo)
        haber_cuentasporpagar=0        
        print("DEBE: ", debe_cuentasporpagar)
        print("HABER: ", haber_cuentasporpagar)
    else:
        debe_cuentasporpagar=0
        haber_cuentasporpagar=0
        print("DEBE: ", debe_cuentasporpagar)
        print("HABER: ", haber_cuentasporpagar)

    #Préstamos a pagar
    print("\nPréstamos por pagar: ")
    cuenta_prestamosporpagar = Cuenta.objects.get(nombre="Prestamos por pagar")  

    if cuenta_prestamosporpagar.saldo<0 and cuenta_prestamosporpagar.clase.nombre == "Pasivo":
        debe_prestamosporpagar=0
        haber_prestamosporpagar=abs(cuenta_prestamosporpagar.saldo)        
        print("DEBE: ", debe_prestamosporpagar)
        print("HABER: ", haber_prestamosporpagar)
    elif cuenta_prestamosporpagar.saldo>0 and cuenta_prestamosporpagar.clase.nombre == "Pasivo":
        debe_prestamosporpagar=abs(cuenta_prestamosporpagar.saldo)
        haber_prestamosporpagar=0        
        print("DEBE: ", debe_prestamosporpagar)
        print("HABER: ", haber_prestamosporpagar)
    else:
        debe_prestamosporpagar=0
        haber_prestamosporpagar=0
        print("DEBE: ", debe_prestamosporpagar)
        print("HABER: ", haber_prestamosporpagar)

    #Sobregiros bancarios
    print("\nSobregiros bancarios: ")
    cuenta_sobregirosbancarios = Cuenta.objects.get(nombre="Sobregiros bancarios")  

    if cuenta_sobregirosbancarios.saldo<0 and cuenta_sobregirosbancarios.clase.nombre == "Pasivo":
        debe_sobregirosbancarios=0
        haber_sobregirosbancarios=abs(cuenta_sobregirosbancarios.saldo)        
        print("DEBE: ", debe_sobregirosbancarios)
        print("HABER: ", haber_sobregirosbancarios)
    elif cuenta_sobregirosbancarios.saldo>0 and cuenta_sobregirosbancarios.clase.nombre == "Pasivo":
        debe_sobregirosbancarios=abs(cuenta_sobregirosbancarios.saldo)
        haber_sobregirosbancarios=0        
        print("DEBE: ", debe_sobregirosbancarios)
        print("HABER: ", haber_sobregirosbancarios)
    else:
        debe_sobregirosbancarios=0
        haber_sobregirosbancarios=0
        print("DEBE: ", debe_sobregirosbancarios)
        print("HABER: ", haber_sobregirosbancarios)

    #Otros títulos valores
    print("\nOtros títulos valores: ")
    cuenta_otrostitulosvalores = Cuenta.objects.get(nombre="Otros titulos valores")  

    if cuenta_otrostitulosvalores.saldo<0 and cuenta_otrostitulosvalores.clase.nombre == "Pasivo":
        debe_otrostitulosvalores=0
        haber_otrostitulosvalores=abs(cuenta_otrostitulosvalores.saldo)        
        print("DEBE: ", debe_otrostitulosvalores)
        print("HABER: ", haber_otrostitulosvalores)
    elif cuenta_otrostitulosvalores.saldo>0 and cuenta_otrostitulosvalores.clase.nombre == "Pasivo":
        debe_otrostitulosvalores=abs(cuenta_otrostitulosvalores.saldo)
        haber_otrostitulosvalores=0        
        print("DEBE: ", debe_otrostitulosvalores)
        print("HABER: ", haber_otrostitulosvalores)
    else:
        debe_otrostitulosvalores=0
        haber_otrostitulosvalores=0
        print("DEBE: ", debe_otrostitulosvalores)
        print("HABER: ", haber_otrostitulosvalores)

    #ISSS
    print("\nISSS: ")
    cuenta_ISSS = Cuenta.objects.get(nombre="ISSS")  

    if cuenta_ISSS.saldo<0 and cuenta_ISSS.clase.nombre == "Pasivo":
        debe_ISSS=0
        haber_ISSS=abs(cuenta_ISSS.saldo)        
        print("DEBE: ", debe_ISSS)
        print("HABER: ", haber_ISSS)
    elif cuenta_ISSS.saldo>0 and cuenta_ISSS.clase.nombre == "Pasivo":
        debe_ISSS=abs(cuenta_ISSS.saldo)
        haber_ISSS=0        
        print("DEBE: ", debe_ISSS)
        print("HABER: ", haber_ISSS)
    else:
        debe_ISSS=0
        haber_ISSS=0
        print("DEBE: ", debe_ISSS)
        print("HABER: ", haber_ISSS)

    #AFP
    print("\nAFP: ")
    cuenta_AFP = Cuenta.objects.get(nombre="AFP")  

    if cuenta_AFP.saldo<0 and cuenta_AFP.clase.nombre == "Pasivo":
        debe_AFP=0
        haber_AFP=abs(cuenta_AFP.saldo)        
        print("DEBE: ", debe_AFP)
        print("HABER: ", haber_AFP)
    elif cuenta_AFP.saldo>0 and cuenta_AFP.clase.nombre == "Pasivo":
        debe_AFP=abs(cuenta_AFP.saldo)
        haber_AFP=0        
        print("DEBE: ", debe_AFP)
        print("HABER: ", haber_AFP)
    else:
        debe_AFP=0
        haber_AFP=0
        print("DEBE: ", debe_AFP)
        print("HABER: ", haber_AFP)

    #AFP
    print("\nRenta: ")
    cuenta_renta = Cuenta.objects.get(nombre="Renta")  

    if cuenta_renta.saldo<0 and cuenta_renta.clase.nombre == "Pasivo":
        debe_renta=0
        haber_renta=abs(cuenta_renta.saldo)        
        print("DEBE: ", debe_renta)
        print("HABER: ", haber_renta)
    elif cuenta_renta.saldo>0 and cuenta_renta.clase.nombre == "Pasivo":
        debe_renta=abs(cuenta_renta.saldo)
        haber_renta=0        
        print("DEBE: ", debe_renta)
        print("HABER: ", haber_renta)
    else:
        debe_renta=0
        haber_renta=0
        print("DEBE: ", debe_renta)
        print("HABER: ", haber_renta)

    #IVA
    print("\nIVA: ")
    cuenta_IVA = Cuenta.objects.get(nombre="IVA")  

    if cuenta_IVA.saldo<0 and cuenta_IVA.clase.nombre == "Pasivo":
        debe_IVA=0
        haber_IVA=abs(cuenta_IVA.saldo)        
        print("DEBE: ", debe_IVA)
        print("HABER: ", haber_IVA)
    elif cuenta_IVA.saldo>0 and cuenta_IVA.clase.nombre == "Pasivo":
        debe_IVA=abs(cuenta_IVA.saldo)
        haber_IVA=0        
        print("DEBE: ", debe_IVA)
        print("HABER: ", haber_IVA)
    else:
        debe_IVA=0
        haber_IVA=0
        print("DEBE: ", debe_IVA)
        print("HABER: ", haber_IVA)

    #Iva debito fiscal
    print("\nIva debito fiscal: ")
    cuenta_ivadebitofiscal = Cuenta.objects.get(nombre="Iva debito fiscal")  

    if cuenta_ivadebitofiscal.saldo<0 and cuenta_ivadebitofiscal.clase.nombre == "Pasivo":
        debe_ivadebitofiscal=0
        haber_ivadebitofiscal=abs(cuenta_ivadebitofiscal.saldo)        
        print("DEBE: ", debe_ivadebitofiscal)
        print("HABER: ", haber_ivadebitofiscal)
    elif cuenta_ivadebitofiscal.saldo>0 and cuenta_ivadebitofiscal.clase.nombre == "Pasivo":
        debe_ivadebitofiscal=abs(cuenta_IVA.saldo)
        haber_ivadebitofiscal=0        
        print("DEBE: ", debe_ivadebitofiscal)
        print("HABER: ", haber_ivadebitofiscal)
    else:
        debe_ivadebitofiscal=0
        haber_ivadebitofiscal=0
        print("DEBE: ", debe_ivadebitofiscal)
        print("HABER: ", haber_ivadebitofiscal)

    #Intereses percibidos
    print("\nIntereses percibidos: ")
    cuenta_interesespercibidos = Cuenta.objects.get(nombre="Intereses percibidos")  

    if cuenta_interesespercibidos.saldo<0 and cuenta_interesespercibidos.clase.nombre == "Pasivo":
        debe_interesespercibidos=0
        haber_interesespercibidos=abs(cuenta_interesespercibidos.saldo)        
        print("DEBE: ", debe_interesespercibidos)
        print("HABER: ", haber_interesespercibidos)
    elif cuenta_interesespercibidos.saldo>0 and cuenta_interesespercibidos.clase.nombre == "Pasivo":
        debe_interesespercibidos=abs(cuenta_interesespercibidos.saldo)
        haber_interesespercibidos=0        
        print("DEBE: ", debe_interesespercibidos)
        print("HABER: ", haber_interesespercibidos)
    else:
        debe_interesespercibidos=0
        haber_interesespercibidos=0
        print("DEBE: ", debe_interesespercibidos)
        print("HABER: ", haber_interesespercibidos)

    #Documentos por pagar
    print("\nDocumentos por pagar: ")
    cuenta_documentosporpagar = Cuenta.objects.get(nombre="Documentos por pagar")  

    if cuenta_documentosporpagar.saldo<0 and cuenta_documentosporpagar.clase.nombre == "Pasivo":
        debe_documentosporpagar=0
        haber_documentosporpagar=abs(cuenta_documentosporpagar.saldo)        
        print("DEBE: ", debe_documentosporpagar)
        print("HABER: ", haber_documentosporpagar)
    elif cuenta_documentosporpagar.saldo>0 and cuenta_documentosporpagar.clase.nombre == "Pasivo":
        debe_documentosporpagar=abs(cuenta_documentosporpagar.saldo)
        haber_documentosporpagar=0        
        print("DEBE: ", debe_documentosporpagar)
        print("HABER: ", haber_documentosporpagar)
    else:
        debe_documentosporpagar=0
        haber_documentosporpagar=0
        print("DEBE: ", debe_documentosporpagar)
        print("HABER: ", haber_documentosporpagar)


    #Capital 
    print("\ncapital: ")
    cuenta_capital = Cuenta.objects.get(nombre="Capital")
    
    if cuenta_capital.saldo<0 and cuenta_capital.clase.nombre == "Patrimonio":
        debe_capital=0
        haber_capital=abs(cuenta_capital.saldo)        
        print("DEBE: ", debe_capital)
        print("HABER: ", haber_capital)
    elif cuenta_capital.saldo>0 and cuenta_capital.clase.nombre == "Patrimonio":
        debe_capital=abs(cuenta_capital.saldo)
        haber_capital=0        
        print("DEBE: ", debe_capital)
        print("HABER: ", haber_capital)
    else:
        debe_capital=0
        haber_capital=0
        print("DEBE: ", debe_capital)
        print("HABER: ", haber_capital)

    #Resultados deudoras
    #Costos por servicios (pasivo)
    print("\nCostos por servicios: ")
    cuenta_costosporservicios = Cuenta.objects.get(nombre="Costos por servicios")  

    if cuenta_costosporservicios.saldo<0 and cuenta_costosporservicios.clase.nombre == "Resultado":
        debe_costosporservicios=0
        haber_costosporservicios=abs(cuenta_costosporservicios.saldo)        
        print("DEBE: ", debe_costosporservicios)
        print("HABER: ", haber_costosporservicios)
    elif cuenta_costosporservicios.saldo>0 and cuenta_costosporservicios.clase.nombre == "Resultado":
        debe_costosporservicios=abs(cuenta_costosporservicios.saldo)
        haber_costosporservicios=0        
        print("DEBE: ", debe_costosporservicios)
        print("HABER: ", haber_costosporservicios)
    else:
        debe_costosporservicios=0
        haber_costosporservicios=0
        print("DEBE: ", debe_costosporservicios)
        print("HABER: ", haber_costosporservicios)

    #Documentos sobre ventas (pasivo)
    print("\nDescuentos sobre ventas: ")
    cuenta_descuentossobreventas = Cuenta.objects.get(nombre="Descuentos sobre ventas") 
    
    if cuenta_descuentossobreventas.saldo<0 and cuenta_descuentossobreventas.clase.nombre == "Resultado":
        debe_descuentossobreventas=0
        haber_descuentossobreventas=abs(cuenta_descuentossobreventas.saldo)        
        print("DEBE: ", debe_descuentossobreventas)
        print("HABER: ", haber_descuentossobreventas)
    elif cuenta_descuentossobreventas.saldo>0 and cuenta_descuentossobreventas.clase.nombre == "Resultado":
        debe_descuentossobreventas=abs(cuenta_descuentossobreventas.saldo)
        haber_descuentossobreventas=0        
        print("DEBE: ", debe_descuentossobreventas)
        print("HABER: ", haber_descuentossobreventas)
    else:
        debe_descuentossobreventas=0
        haber_descuentossobreventas=0
        print("DEBE: ", debe_descuentossobreventas)
        print("HABER: ", haber_descuentossobreventas)

    #Gastos
    #Gastos de administracion (pasivo) 
    print("\nGastos de administracion: ")
    cuenta_gastosdeadministracion = Cuenta.objects.get(nombre="Gastos de administracion")  

    if cuenta_gastosdeadministracion.saldo<0 and cuenta_gastosdeadministracion.clase.nombre == "Resultado":
        debe_gastosdeadministracion=0
        haber_gastosdeadministracion=abs(cuenta_gastosdeadministracion.saldo)        
        print("DEBE: ", debe_gastosdeadministracion)
        print("HABER: ", haber_gastosdeadministracion)
    elif cuenta_gastosdeadministracion.saldo>0 and cuenta_gastosdeadministracion.clase.nombre == "Resultado":
        debe_gastosdeadministracion=abs(cuenta_gastosdeadministracion.saldo)
        haber_gastosdeadministracion=0        
        print("DEBE: ", debe_gastosdeadministracion)
        print("HABER: ", haber_gastosdeadministracion)
    else:
        debe_gastosdeadministracion=0
        haber_gastosdeadministracion=0
        print("DEBE: ", debe_gastosdeadministracion)
        print("HABER: ", haber_gastosdeadministracion)

    #Sueldos y salarios (pasivo) 
    print("\nSueldos y salarios: ")
    cuenta_sueldosysalarios = Cuenta.objects.get(nombre="Sueldos y salarios")  

    if cuenta_sueldosysalarios.saldo<0 and cuenta_sueldosysalarios.clase.nombre == "Resultado":
        debe_sueldosysalarios=0
        haber_sueldosysalarios=abs(cuenta_sueldosysalarios.saldo)        
        print("DEBE: ", debe_sueldosysalarios)
        print("HABER: ", haber_sueldosysalarios)
    elif cuenta_sueldosysalarios.saldo>0 and cuenta_sueldosysalarios.clase.nombre == "Resultado":
        debe_sueldosysalarios=abs(cuenta_sueldosysalarios.saldo)
        haber_sueldosysalarios=0        
        print("DEBE: ", debe_sueldosysalarios)
        print("HABER: ", haber_sueldosysalarios)
    else:
        debe_sueldosysalarios=0
        haber_sueldosysalarios=0
        print("DEBE: ", debe_sueldosysalarios)
        print("HABER: ", haber_sueldosysalarios)

    #Mantenimiento de equipo (pasivo) 
    print("\nMantenimiento de equipo: ")
    cuenta_mantenimientodeequipo = Cuenta.objects.get(nombre="Mantenimiento de equipo")  

    if cuenta_mantenimientodeequipo.saldo<0 and cuenta_mantenimientodeequipo.clase.nombre == "Resultado":
        debe_mantenimientodeequipo=0
        haber_mantenimientodeequipo=abs(cuenta_mantenimientodeequipo.saldo)        
        print("DEBE: ", debe_mantenimientodeequipo)
        print("HABER: ", haber_mantenimientodeequipo)
    elif cuenta_mantenimientodeequipo.saldo>0 and cuenta_mantenimientodeequipo.clase.nombre == "Resultado":
        debe_mantenimientodeequipo=abs(cuenta_mantenimientodeequipo.saldo)
        haber_mantenimientodeequipo=0        
        print("DEBE: ", debe_mantenimientodeequipo)
        print("HABER: ", haber_mantenimientodeequipo)
    else:
        debe_mantenimientodeequipo=0
        haber_mantenimientodeequipo=0
        print("DEBE: ", debe_mantenimientodeequipo)
        print("HABER: ", haber_mantenimientodeequipo)

    #Cuentas de resultado acreedoras
    #Ventas (pasivo) 
    print("\nVentas: ")
    cuenta_ventas = Cuenta.objects.get(nombre="Ventas")
    
    if cuenta_ventas.saldo>0 and cuenta_ventas.clase.nombre == "Activo":
        debe_ventas=abs(cuenta_ventas.saldo)
        haber_ventas=0
        print("DEBE: ", debe_ventas)
        print("HABER: ", haber_ventas)
    elif cuenta_ventas.saldo<0 and cuenta_ventas.clase.nombre == "Activo":
        debe_ventas=0
        haber_ventas=abs(cuenta_ventas.saldo)
        print("DEBE: ", debe_ventas)
        print("HABER: ", haber_ventas)
    else:
        debe_ventas=0
        haber_ventas=0
        print("DEBE: ", debe_ventas)
        print("HABER: ", haber_ventas)

    #Calculo total activos
    debe_total_activos=debe_efectivo+debe_bancos+debe_cuentasporcobrar+debe_documentosporcobrar+debe_interesesporcobrar+debe_gastospagadosporadelantado+debe_papeleriayutiles+debe_ivacreditofiscal+debe_ivapagadoporanticipado+debe_insumos+debe_equipoinformatico
    haber_total_activos=haber_efectivo+haber_bancos+haber_cuentasporcobrar+haber_documentosporcobrar+haber_interesesporcobrar+haber_gastospagadosporadelantado+haber_papeleriayutiles+haber_ivacreditofiscal+haber_ivapagadoporanticipado+haber_insumos+haber_equipoinformatico     

    #Calculo total pasivos + capital
    debe_total_pasivos=debe_cuentasporpagar+debe_prestamosporpagar+debe_prestamosporpagar+debe_otrostitulosvalores+debe_ISSS+debe_AFP+debe_renta+debe_IVA+debe_ivadebitofiscal+debe_interesespercibidos+debe_documentosporpagar+debe_capital
    haber_total_pasivos=haber_cuentasporpagar+haber_prestamosporpagar+haber_prestamosporpagar+haber_otrostitulosvalores+haber_ISSS+haber_AFP+haber_renta+haber_IVA+haber_ivadebitofiscal+haber_interesespercibidos+haber_documentosporpagar+haber_capital

    #Totales generales
    debe_total=debe_total_activos+debe_total_pasivos
    haber_total=haber_total_activos+haber_total_pasivos


    return render(request, 'transacciones/balanza_comprobacion.html', {
        # ----------sALIDAS PARA EL BALANCE DE COMPROBACION----------------------#
        #Activos
        #Activos corrientes
        'debe_efectivo': debe_efectivo,
        'haber_efectivo': haber_efectivo,
        'debe_bancos': debe_bancos,
        'haber_bancos': haber_bancos,
        'debe_cuentasporcobrar': debe_cuentasporcobrar,
        'haber_cuentasporcobrar': haber_cuentasporcobrar,
        'debe_documentosporcobrar': debe_documentosporcobrar,
        'haber_documentosporcobrar': haber_documentosporcobrar,
        'debe_interesesporcobrar': debe_interesesporcobrar,
        'haber_interesesporcobrar': haber_interesesporcobrar,
        'debe_gastospagadosporadelantado': debe_gastospagadosporadelantado,
        'haber_gastospagadosporadelantado': haber_gastospagadosporadelantado,
        'debe_papeleriayutiles': debe_papeleriayutiles,
        'haber_papeleriayutiles': haber_papeleriayutiles,
        'debe_ivacreditofiscal': debe_ivacreditofiscal,
        'haber_ivacreditofiscal': haber_ivacreditofiscal,
        #Activos no corrientes
        'debe_insumos': debe_insumos,
        'haber_insumos': haber_insumos,
        'debe_equipoinformatico': debe_equipoinformatico,
        'haber_equipoinformatico': haber_equipoinformatico,

        #Pasivos
        'debe_cuentasporpagar': debe_cuentasporpagar,
        'haber_cuentasporpagar': haber_cuentasporpagar,
        'debe_prestamosporpagar': debe_prestamosporpagar,
        'haber_prestamosporpagar': haber_prestamosporpagar,
        'debe_sobregirosbancarios': debe_sobregirosbancarios,
        'haber_sobregirosbancarios': haber_sobregirosbancarios,
        'debe_otrostitulosvalores': debe_otrostitulosvalores,
        'haber_otrostitulosvalores': haber_otrostitulosvalores,
        'debe_ISSS': debe_ISSS,
        'haber_ISSS': haber_ISSS,
        'debe_AFP': debe_AFP,
        'haber_AFP': haber_AFP,
        'debe_renta': debe_renta,
        'haber_renta': haber_renta,
        'debe_IVA': debe_IVA,
        'haber_IVA': haber_IVA,
        'debe_ivadebitofiscal': debe_ivadebitofiscal,
        'haber_ivadebitofiscal': haber_ivadebitofiscal,
        'debe_interesespercibidos': debe_interesespercibidos,
        'haber_interesespercibidos': haber_interesespercibidos,
        'debe_documentosporpagar': debe_documentosporpagar,
        'haber_documentosporpagar': haber_documentosporpagar,

        #Capital
        'debe_capital': debe_capital,
        'haber_capital': haber_capital,

        #Resultados deudoras
        'debe_costosporservicios': debe_costosporservicios,
        'haber_costosporservicios': haber_costosporservicios,
        'debe_descuentossobreventas': debe_descuentossobreventas,
        'haber_descuentossobreventas': haber_descuentossobreventas,
        'debe_gastosdeadministracion': debe_gastosdeadministracion,
        'haber_gastosdeadministracion': haber_gastosdeadministracion,
        'debe_sueldosysalarios': debe_sueldosysalarios,
        'haber_sueldosysalarios': haber_sueldosysalarios,
        'debe_mantenimientodeequipo': debe_mantenimientodeequipo,
        'haber_mantenimientodeequipo': haber_mantenimientodeequipo,

        #Resultados acreedoras
        'debe_ventas': debe_ventas,
        'haber_ventas': haber_ventas,

        #totales
        'debe_total_activos': debe_total_activos,
        'haber_total_activos': haber_total_activos,
        #total pasivos + capital
        'debe_total_pasivos': debe_total_pasivos,
        'haber_total_pasivos': haber_total_pasivos,
        #tatales generales
        'debe_total': debe_total,
        'haber_total': haber_total,

        'transacciones': transacciones,        
        'balance': balance,
    })


def hojaTrabajo(request):
    #Obtener el titulo de Balance para ser actualizado al momento de hacer un ajuste
    titulo='Balance de Comprobación'

    #logica para el registro de AJUSTES
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            titulo='Balance de Comprobación Ajustado'

            form.save()
            # Puedes redirigir a una página de confirmación o hacer lo que necesites
            #redirect('transacciones/registro_transaccion.html')
    else:
        form = TransaccionForm()

    # Cargar opciones de clases de cuentas y cuentas desde la base de datos
    clases_de_cuentas = ClaseCuenta.objects.all()
    cuentas = Cuenta.objects.all()

   
    # -------------LOGICA PARA EL BALANCE DE COMPROBACION------------------ # 
    #Activos
    #Activos corrientes
    #Efectivo
    print("\nefectivo: ")
    cuenta_efectivo = Cuenta.objects.get(nombre="Efectivo")

    if cuenta_efectivo.saldo>0 and cuenta_efectivo.clase.nombre == "Activo":
        debe_efectivo=abs(cuenta_efectivo.saldo)
        haber_efectivo=0
        print("DEBE: ", debe_efectivo)
        print("HABER: ", haber_efectivo)
    elif cuenta_efectivo.saldo<0 and cuenta_efectivo.clase.nombre == "Activo":
        debe_efectivo=0
        haber_efectivo=abs(cuenta_efectivo.saldo)
        print("DEBE: ", debe_efectivo)
        print("HABER: ", haber_efectivo)
    else:
        debe_efectivo=0
        haber_efectivo=0
        print("DEBE: ", debe_efectivo)
        print("HABER: ", haber_efectivo)

    #Bancos
    print("\nbancos: ")
    cuenta_bancos = Cuenta.objects.get(nombre="Bancos")

    if cuenta_bancos.saldo>0 and cuenta_bancos.clase.nombre == "Activo":
        debe_bancos=abs(cuenta_bancos.saldo)
        haber_bancos=0
        print("DEBE: ", debe_bancos)
        print("HABER: ", haber_bancos)
    elif cuenta_bancos.saldo<0 and cuenta_bancos.clase.nombre == "Activo":
        debe_bancos=0
        haber_bancos=abs(cuenta_bancos.saldo)
        print("DEBE: ", debe_bancos)
        print("HABER: ", haber_bancos)
    else:
        debe_bancos=0
        haber_bancos=0
        print("DEBE: ", debe_bancos)
        print("HABER: ", haber_bancos)

    #Cuentas por cobrar
    print("\nCuentas por cobrar: ")
    cuenta_cuentasporcobrar = Cuenta.objects.get(nombre="Cuentas por cobrar")

    if cuenta_cuentasporcobrar.saldo>0 and cuenta_cuentasporcobrar.clase.nombre == "Activo":
        debe_cuentasporcobrar=abs(cuenta_cuentasporcobrar.saldo)
        haber_cuentasporcobrar=0
        print("DEBE: ", debe_cuentasporcobrar)
        print("HABER: ", haber_cuentasporcobrar)
    elif cuenta_cuentasporcobrar.saldo<0 and cuenta_cuentasporcobrar.clase.nombre == "Activo":
        debe_cuentasporcobrar=0
        haber_cuentasporcobrar=abs(cuenta_cuentasporcobrar.saldo)
        print("DEBE: ", debe_cuentasporcobrar)
        print("HABER: ", haber_cuentasporcobrar)
    else:
        debe_cuentasporcobrar=0
        haber_cuentasporcobrar=0
        print("DEBE: ", debe_cuentasporcobrar)
        print("HABER: ", haber_cuentasporcobrar)

    #Documentos por cobrar
    cuenta_documentosporcobrar = Cuenta.objects.get(nombre="Documentos por cobrar")
    print("\nDocumentos por cobrar")

    if cuenta_documentosporcobrar.saldo>0 and cuenta_documentosporcobrar.clase.nombre == "Activo":
        debe_documentosporcobrar=abs(cuenta_documentosporcobrar.saldo)
        haber_documentosporcobrar=0
        print("DEBE: ", debe_documentosporcobrar)
        print("HABER: ", haber_documentosporcobrar)
    elif cuenta_documentosporcobrar.saldo<0 and cuenta_documentosporcobrar.clase.nombre == "Activo":
        debe_documentosporcobrar=0
        haber_documentosporcobrar=abs(cuenta_documentosporcobrar.saldo)
        print("DEBE: ", debe_documentosporcobrar)
        print("HABER: ", haber_documentosporcobrar)
    else:
        debe_documentosporcobrar=0
        haber_documentosporcobrar=0
        print("DEBE: ", debe_documentosporcobrar)
        print("HABER: ", haber_documentosporcobrar)

    #Intereses por cobrar
    cuenta_interesesporcobrar = Cuenta.objects.get(nombre="Intereses por cobrar")
    print("\nIntereses por cobrar")

    if cuenta_interesesporcobrar.saldo>0 and cuenta_interesesporcobrar.clase.nombre == "Activo":
        debe_interesesporcobrar=abs(cuenta_interesesporcobrar.saldo)
        haber_interesesporcobrar=0
        print("DEBE: ", debe_interesesporcobrar)
        print("HABER: ", haber_interesesporcobrar)
    elif cuenta_interesesporcobrar.saldo<0 and cuenta_interesesporcobrar.clase.nombre == "Activo":
        debe_interesesporcobrar=0
        haber_interesesporcobrar=abs(cuenta_interesesporcobrar.saldo)
        print("DEBE: ", debe_interesesporcobrar)
        print("HABER: ", haber_interesesporcobrar)
    else:
        debe_interesesporcobrar=0
        haber_interesesporcobrar=0
        print("DEBE: ", debe_interesesporcobrar)
        print("HABER: ", haber_interesesporcobrar)
   
    #Gastos pagados por adelantado
    cuenta_gastospagadosporadelantado = Cuenta.objects.get(nombre="Gastos pagados por adelantado")
    print("\nGastos pagados por adelantado")

    if cuenta_gastospagadosporadelantado.saldo>0 and cuenta_gastospagadosporadelantado.clase.nombre == "Activo":
        debe_gastospagadosporadelantado=abs(cuenta_gastospagadosporadelantado.saldo)
        haber_gastospagadosporadelantado=0
        print("DEBE: ", debe_gastospagadosporadelantado)
        print("HABER: ", haber_gastospagadosporadelantado)
    elif cuenta_gastospagadosporadelantado.saldo<0 and cuenta_gastospagadosporadelantado.clase.nombre == "Activo":
        debe_gastospagadosporadelantado=0
        haber_gastospagadosporadelantado=abs(cuenta_gastospagadosporadelantado.saldo)
        print("DEBE: ", debe_gastospagadosporadelantado)
        print("HABER: ", haber_gastospagadosporadelantado)
    else:
        debe_gastospagadosporadelantado=0
        haber_gastospagadosporadelantado=0
        print("DEBE: ", debe_gastospagadosporadelantado)
        print("HABER: ", haber_gastospagadosporadelantado)

    #Papeleria y utiles
    cuenta_papeleriayutiles = Cuenta.objects.get(nombre="Papelería y útiles")
    print("\nPapeleria y utiles")

    if cuenta_papeleriayutiles.saldo>0 and cuenta_papeleriayutiles.clase.nombre == "Activo":
        debe_papeleriayutiles=abs(cuenta_papeleriayutiles.saldo)
        haber_papeleriayutiles=0
        print("DEBE: ", debe_papeleriayutiles)
        print("HABER: ", haber_papeleriayutiles)
    elif cuenta_papeleriayutiles.saldo<0 and cuenta_papeleriayutiles.clase.nombre == "Activo":
        debe_papeleriayutiles=0
        haber_papeleriayutiles=abs(cuenta_papeleriayutiles.saldo)
        print("DEBE: ", debe_papeleriayutiles)
        print("HABER: ", haber_papeleriayutiles)
    else:
        debe_papeleriayutiles=0
        haber_papeleriayutiles=0
        print("DEBE: ", debe_papeleriayutiles)
        print("HABER: ", haber_papeleriayutiles)

    #Iva credito fiscal
    print("\nIva credito fiscal")
    cuenta_ivacreditofiscal = Cuenta.objects.get(nombre="Iva credito fiscal")

    if cuenta_ivacreditofiscal.saldo>0 and cuenta_ivacreditofiscal.clase.nombre == "Activo":
        debe_ivacreditofiscal=abs(cuenta_ivacreditofiscal.saldo)
        haber_ivacreditofiscal=0
        print("DEBE: ", debe_ivacreditofiscal)
        print("HABER: ", haber_ivacreditofiscal)
    elif cuenta_ivacreditofiscal.saldo<0 and cuenta_ivacreditofiscal.clase.nombre == "Activo":
        debe_ivacreditofiscal=0
        haber_ivacreditofiscal=abs(cuenta_ivacreditofiscal.saldo)
        print("DEBE: ", debe_ivacreditofiscal)
        print("HABER: ", haber_ivacreditofiscal)
    else:
        debe_ivacreditofiscal=0
        haber_ivacreditofiscal=0
        print("DEBE: ", debe_ivacreditofiscal)
        print("HABER: ", haber_ivacreditofiscal)

    #Iva pagado por anticipado
    print("\nIva pagado por anticipado")
    cuenta_ivapagadoporanticipado = Cuenta.objects.get(nombre="IVA pagado por anticipado")

    if cuenta_ivapagadoporanticipado.saldo>0 and cuenta_ivapagadoporanticipado.clase.nombre == "Activo":
        debe_ivapagadoporanticipado=abs(cuenta_ivapagadoporanticipado.saldo)
        haber_ivapagadoporanticipado=0
        print("DEBE: ", debe_ivapagadoporanticipado)
        print("HABER: ", haber_ivapagadoporanticipado)
    elif cuenta_ivapagadoporanticipado.saldo<0 and cuenta_ivapagadoporanticipado.clase.nombre == "Activo":
        debe_ivapagadoporanticipado=0
        haber_ivapagadoporanticipado=abs(cuenta_ivapagadoporanticipado.saldo)
        print("DEBE: ", debe_ivapagadoporanticipado)
        print("HABER: ", haber_ivapagadoporanticipado)
    else:
        debe_ivapagadoporanticipado=0
        haber_ivapagadoporanticipado=0
        print("DEBE: ", debe_ivapagadoporanticipado)
        print("HABER: ", haber_ivapagadoporanticipado)

    #No corrientes
    #Insumos
    print("\nInsumos: ")
    cuenta_insumos = Cuenta.objects.get(nombre="Insumos")
    
    if cuenta_insumos.saldo>0 and cuenta_insumos.clase.nombre == "Activo":
        debe_insumos=abs(cuenta_insumos.saldo)
        haber_insumos=0
        print("DEBE: ", debe_insumos)
        print("HABER: ", haber_insumos)
    elif cuenta_insumos.saldo<0 and cuenta_insumos.clase.nombre == "Activo":
        debe_insumos=0
        haber_insumos=abs(cuenta_insumos.saldo)
        print("DEBE: ", debe_insumos)
        print("HABER: ", haber_insumos)
    else:
        debe_insumos=0
        haber_insumos=0
        print("DEBE: ", debe_insumos)
        print("HABER: ", haber_insumos)

    #Equipo informatico
    print("\nEquipo informatico: ")
    cuenta_equipoinformatico = Cuenta.objects.get(nombre="Equipo Informatico")
    
    if cuenta_equipoinformatico.saldo>0 and cuenta_equipoinformatico.clase.nombre == "Activo":
        debe_equipoinformatico=abs(cuenta_equipoinformatico.saldo)
        haber_equipoinformatico=0
        print("DEBE: ", debe_equipoinformatico)
        print("HABER: ", haber_equipoinformatico)
    elif cuenta_equipoinformatico.saldo<0 and cuenta_equipoinformatico.clase.nombre == "Activo":
        debe_equipoinformatico=0
        haber_equipoinformatico=abs(cuenta_equipoinformatico.saldo)
        print("DEBE: ", debe_equipoinformatico)
        print("HABER: ", haber_equipoinformatico)
    else:
        debe_equipoinformatico=0
        haber_equipoinformatico=0
        print("DEBE: ", debe_equipoinformatico)
        print("HABER: ", haber_equipoinformatico)

    #Pasivo
    #Corriente
    #Cuentas por pagar
    print("\nCuentas por pagar: ")
    cuenta_cuentasporpagar = Cuenta.objects.get(nombre="Cuentas por pagar")  

    if cuenta_cuentasporpagar.saldo<0 and cuenta_cuentasporpagar.clase.nombre == "Pasivo":
        debe_cuentasporpagar=0
        haber_cuentasporpagar=abs(cuenta_cuentasporpagar.saldo)        
        print("DEBE: ", debe_cuentasporpagar)
        print("HABER: ", haber_cuentasporpagar)
    elif cuenta_cuentasporpagar.saldo>0 and cuenta_cuentasporpagar.clase.nombre == "Pasivo":
        debe_cuentasporpagar=abs(cuenta_cuentasporpagar.saldo)
        haber_cuentasporpagar=0        
        print("DEBE: ", debe_cuentasporpagar)
        print("HABER: ", haber_cuentasporpagar)
    else:
        debe_cuentasporpagar=0
        haber_cuentasporpagar=0
        print("DEBE: ", debe_cuentasporpagar)
        print("HABER: ", haber_cuentasporpagar)

    #Préstamos a pagar
    print("\nPréstamos por pagar: ")
    cuenta_prestamosporpagar = Cuenta.objects.get(nombre="Prestamos por pagar")  

    if cuenta_prestamosporpagar.saldo<0 and cuenta_prestamosporpagar.clase.nombre == "Pasivo":
        debe_prestamosporpagar=0
        haber_prestamosporpagar=abs(cuenta_prestamosporpagar.saldo)        
        print("DEBE: ", debe_prestamosporpagar)
        print("HABER: ", haber_prestamosporpagar)
    elif cuenta_prestamosporpagar.saldo>0 and cuenta_prestamosporpagar.clase.nombre == "Pasivo":
        debe_prestamosporpagar=abs(cuenta_prestamosporpagar.saldo)
        haber_prestamosporpagar=0        
        print("DEBE: ", debe_prestamosporpagar)
        print("HABER: ", haber_prestamosporpagar)
    else:
        debe_prestamosporpagar=0
        haber_prestamosporpagar=0
        print("DEBE: ", debe_prestamosporpagar)
        print("HABER: ", haber_prestamosporpagar)

    #Sobregiros bancarios
    print("\nSobregiros bancarios: ")
    cuenta_sobregirosbancarios = Cuenta.objects.get(nombre="Sobregiros bancarios")  

    if cuenta_sobregirosbancarios.saldo<0 and cuenta_sobregirosbancarios.clase.nombre == "Pasivo":
        debe_sobregirosbancarios=0
        haber_sobregirosbancarios=abs(cuenta_sobregirosbancarios.saldo)        
        print("DEBE: ", debe_sobregirosbancarios)
        print("HABER: ", haber_sobregirosbancarios)
    elif cuenta_sobregirosbancarios.saldo>0 and cuenta_sobregirosbancarios.clase.nombre == "Pasivo":
        debe_sobregirosbancarios=abs(cuenta_sobregirosbancarios.saldo)
        haber_sobregirosbancarios=0        
        print("DEBE: ", debe_sobregirosbancarios)
        print("HABER: ", haber_sobregirosbancarios)
    else:
        debe_sobregirosbancarios=0
        haber_sobregirosbancarios=0
        print("DEBE: ", debe_sobregirosbancarios)
        print("HABER: ", haber_sobregirosbancarios)

    #Otros títulos valores
    print("\nOtros títulos valores: ")
    cuenta_otrostitulosvalores = Cuenta.objects.get(nombre="Otros titulos valores")  

    if cuenta_otrostitulosvalores.saldo<0 and cuenta_otrostitulosvalores.clase.nombre == "Pasivo":
        debe_otrostitulosvalores=0
        haber_otrostitulosvalores=abs(cuenta_otrostitulosvalores.saldo)        
        print("DEBE: ", debe_otrostitulosvalores)
        print("HABER: ", haber_otrostitulosvalores)
    elif cuenta_otrostitulosvalores.saldo>0 and cuenta_otrostitulosvalores.clase.nombre == "Pasivo":
        debe_otrostitulosvalores=abs(cuenta_otrostitulosvalores.saldo)
        haber_otrostitulosvalores=0        
        print("DEBE: ", debe_otrostitulosvalores)
        print("HABER: ", haber_otrostitulosvalores)
    else:
        debe_otrostitulosvalores=0
        haber_otrostitulosvalores=0
        print("DEBE: ", debe_otrostitulosvalores)
        print("HABER: ", haber_otrostitulosvalores)

    #ISSS
    print("\nISSS: ")
    cuenta_ISSS = Cuenta.objects.get(nombre="ISSS")  

    if cuenta_ISSS.saldo<0 and cuenta_ISSS.clase.nombre == "Pasivo":
        debe_ISSS=0
        haber_ISSS=abs(cuenta_ISSS.saldo)        
        print("DEBE: ", debe_ISSS)
        print("HABER: ", haber_ISSS)
    elif cuenta_ISSS.saldo>0 and cuenta_ISSS.clase.nombre == "Pasivo":
        debe_ISSS=abs(cuenta_ISSS.saldo)
        haber_ISSS=0        
        print("DEBE: ", debe_ISSS)
        print("HABER: ", haber_ISSS)
    else:
        debe_ISSS=0
        haber_ISSS=0
        print("DEBE: ", debe_ISSS)
        print("HABER: ", haber_ISSS)

    #AFP
    print("\nAFP: ")
    cuenta_AFP = Cuenta.objects.get(nombre="AFP")  

    if cuenta_AFP.saldo<0 and cuenta_AFP.clase.nombre == "Pasivo":
        debe_AFP=0
        haber_AFP=abs(cuenta_AFP.saldo)        
        print("DEBE: ", debe_AFP)
        print("HABER: ", haber_AFP)
    elif cuenta_AFP.saldo>0 and cuenta_AFP.clase.nombre == "Pasivo":
        debe_AFP=abs(cuenta_AFP.saldo)
        haber_AFP=0        
        print("DEBE: ", debe_AFP)
        print("HABER: ", haber_AFP)
    else:
        debe_AFP=0
        haber_AFP=0
        print("DEBE: ", debe_AFP)
        print("HABER: ", haber_AFP)

    #AFP
    print("\nRenta: ")
    cuenta_renta = Cuenta.objects.get(nombre="Renta")  

    if cuenta_renta.saldo<0 and cuenta_renta.clase.nombre == "Pasivo":
        debe_renta=0
        haber_renta=abs(cuenta_renta.saldo)        
        print("DEBE: ", debe_renta)
        print("HABER: ", haber_renta)
    elif cuenta_renta.saldo>0 and cuenta_renta.clase.nombre == "Pasivo":
        debe_renta=abs(cuenta_renta.saldo)
        haber_renta=0        
        print("DEBE: ", debe_renta)
        print("HABER: ", haber_renta)
    else:
        debe_renta=0
        haber_renta=0
        print("DEBE: ", debe_renta)
        print("HABER: ", haber_renta)

    #IVA
    print("\nIVA: ")
    cuenta_IVA = Cuenta.objects.get(nombre="IVA")  

    if cuenta_IVA.saldo<0 and cuenta_IVA.clase.nombre == "Pasivo":
        debe_IVA=0
        haber_IVA=abs(cuenta_IVA.saldo)        
        print("DEBE: ", debe_IVA)
        print("HABER: ", haber_IVA)
    elif cuenta_IVA.saldo>0 and cuenta_IVA.clase.nombre == "Pasivo":
        debe_IVA=abs(cuenta_IVA.saldo)
        haber_IVA=0        
        print("DEBE: ", debe_IVA)
        print("HABER: ", haber_IVA)
    else:
        debe_IVA=0
        haber_IVA=0
        print("DEBE: ", debe_IVA)
        print("HABER: ", haber_IVA)

    #Iva debito fiscal
    print("\nIva debito fiscal: ")
    cuenta_ivadebitofiscal = Cuenta.objects.get(nombre="Iva debito fiscal")  

    if cuenta_ivadebitofiscal.saldo<0 and cuenta_ivadebitofiscal.clase.nombre == "Pasivo":
        debe_ivadebitofiscal=0
        haber_ivadebitofiscal=abs(cuenta_ivadebitofiscal.saldo)        
        print("DEBE: ", debe_ivadebitofiscal)
        print("HABER: ", haber_ivadebitofiscal)
    elif cuenta_ivadebitofiscal.saldo>0 and cuenta_ivadebitofiscal.clase.nombre == "Pasivo":
        debe_ivadebitofiscal=abs(cuenta_IVA.saldo)
        haber_ivadebitofiscal=0        
        print("DEBE: ", debe_ivadebitofiscal)
        print("HABER: ", haber_ivadebitofiscal)
    else:
        debe_ivadebitofiscal=0
        haber_ivadebitofiscal=0
        print("DEBE: ", debe_ivadebitofiscal)
        print("HABER: ", haber_ivadebitofiscal)

    #Intereses percibidos
    print("\nIntereses percibidos: ")
    cuenta_interesespercibidos = Cuenta.objects.get(nombre="Intereses percibidos")  

    if cuenta_interesespercibidos.saldo<0 and cuenta_interesespercibidos.clase.nombre == "Pasivo":
        debe_interesespercibidos=0
        haber_interesespercibidos=abs(cuenta_interesespercibidos.saldo)        
        print("DEBE: ", debe_interesespercibidos)
        print("HABER: ", haber_interesespercibidos)
    elif cuenta_interesespercibidos.saldo>0 and cuenta_interesespercibidos.clase.nombre == "Pasivo":
        debe_interesespercibidos=abs(cuenta_interesespercibidos.saldo)
        haber_interesespercibidos=0        
        print("DEBE: ", debe_interesespercibidos)
        print("HABER: ", haber_interesespercibidos)
    else:
        debe_interesespercibidos=0
        haber_interesespercibidos=0
        print("DEBE: ", debe_interesespercibidos)
        print("HABER: ", haber_interesespercibidos)

    #Documentos por pagar
    print("\nDocumentos por pagar: ")
    cuenta_documentosporpagar = Cuenta.objects.get(nombre="Documentos por pagar")  

    if cuenta_documentosporpagar.saldo<0 and cuenta_documentosporpagar.clase.nombre == "Pasivo":
        debe_documentosporpagar=0
        haber_documentosporpagar=abs(cuenta_documentosporpagar.saldo)        
        print("DEBE: ", debe_documentosporpagar)
        print("HABER: ", haber_documentosporpagar)
    elif cuenta_documentosporpagar.saldo>0 and cuenta_documentosporpagar.clase.nombre == "Pasivo":
        debe_documentosporpagar=abs(cuenta_documentosporpagar.saldo)
        haber_documentosporpagar=0        
        print("DEBE: ", debe_documentosporpagar)
        print("HABER: ", haber_documentosporpagar)
    else:
        debe_documentosporpagar=0
        haber_documentosporpagar=0
        print("DEBE: ", debe_documentosporpagar)
        print("HABER: ", haber_documentosporpagar)


    #Capital 
    print("\ncapital: ")
    cuenta_capital = Cuenta.objects.get(nombre="Capital")
    
    if cuenta_capital.saldo<0 and cuenta_capital.clase.nombre == "Patrimonio":
        debe_capital=0
        haber_capital=abs(cuenta_capital.saldo)        
        print("DEBE: ", debe_capital)
        print("HABER: ", haber_capital)
    elif cuenta_capital.saldo>0 and cuenta_capital.clase.nombre == "Patrimonio":
        debe_capital=abs(cuenta_capital.saldo)
        haber_capital=0        
        print("DEBE: ", debe_capital)
        print("HABER: ", haber_capital)
    else:
        debe_capital=0
        haber_capital=0
        print("DEBE: ", debe_capital)
        print("HABER: ", haber_capital)

    #Resultados deudoras
    #Costos por servicios (pasivo)
    print("\nCostos por servicios: ")
    cuenta_costosporservicios = Cuenta.objects.get(nombre="Costos por servicios")  

    if cuenta_costosporservicios.saldo<0 and cuenta_costosporservicios.clase.nombre == "Resultado":
        debe_costosporservicios=0
        haber_costosporservicios=abs(cuenta_costosporservicios.saldo)        
        print("DEBE: ", debe_costosporservicios)
        print("HABER: ", haber_costosporservicios)
    elif cuenta_costosporservicios.saldo>0 and cuenta_costosporservicios.clase.nombre == "Resultado":
        debe_costosporservicios=abs(cuenta_costosporservicios.saldo)
        haber_costosporservicios=0        
        print("DEBE: ", debe_costosporservicios)
        print("HABER: ", haber_costosporservicios)
    else:
        debe_costosporservicios=0
        haber_costosporservicios=0
        print("DEBE: ", debe_costosporservicios)
        print("HABER: ", haber_costosporservicios)

    #Documentos sobre ventas (pasivo)
    print("\nDescuentos sobre ventas: ")
    cuenta_descuentossobreventas = Cuenta.objects.get(nombre="Descuentos sobre ventas") 
    
    if cuenta_descuentossobreventas.saldo<0 and cuenta_descuentossobreventas.clase.nombre == "Resultado":
        debe_descuentossobreventas=0
        haber_descuentossobreventas=abs(cuenta_descuentossobreventas.saldo)        
        print("DEBE: ", debe_descuentossobreventas)
        print("HABER: ", haber_descuentossobreventas)
    elif cuenta_descuentossobreventas.saldo>0 and cuenta_descuentossobreventas.clase.nombre == "Resultado":
        debe_descuentossobreventas=abs(cuenta_descuentossobreventas.saldo)
        haber_descuentossobreventas=0        
        print("DEBE: ", debe_descuentossobreventas)
        print("HABER: ", haber_descuentossobreventas)
    else:
        debe_descuentossobreventas=0
        haber_descuentossobreventas=0
        print("DEBE: ", debe_descuentossobreventas)
        print("HABER: ", haber_descuentossobreventas)

    #Gastos
    #Gastos de administracion (pasivo) 
    print("\nGastos de administracion: ")
    cuenta_gastosdeadministracion = Cuenta.objects.get(nombre="Gastos de administracion")  

    if cuenta_gastosdeadministracion.saldo<0 and cuenta_gastosdeadministracion.clase.nombre == "Resultado":
        debe_gastosdeadministracion=0
        haber_gastosdeadministracion=abs(cuenta_gastosdeadministracion.saldo)        
        print("DEBE: ", debe_gastosdeadministracion)
        print("HABER: ", haber_gastosdeadministracion)
    elif cuenta_gastosdeadministracion.saldo>0 and cuenta_gastosdeadministracion.clase.nombre == "Resultado":
        debe_gastosdeadministracion=abs(cuenta_gastosdeadministracion.saldo)
        haber_gastosdeadministracion=0        
        print("DEBE: ", debe_gastosdeadministracion)
        print("HABER: ", haber_gastosdeadministracion)
    else:
        debe_gastosdeadministracion=0
        haber_gastosdeadministracion=0
        print("DEBE: ", debe_gastosdeadministracion)
        print("HABER: ", haber_gastosdeadministracion)

    #Sueldos y salarios (pasivo) 
    print("\nSueldos y salarios: ")
    cuenta_sueldosysalarios = Cuenta.objects.get(nombre="Sueldos y salarios")  

    if cuenta_sueldosysalarios.saldo<0 and cuenta_sueldosysalarios.clase.nombre == "Resultado":
        debe_sueldosysalarios=0
        haber_sueldosysalarios=abs(cuenta_sueldosysalarios.saldo)        
        print("DEBE: ", debe_sueldosysalarios)
        print("HABER: ", haber_sueldosysalarios)
    elif cuenta_sueldosysalarios.saldo>0 and cuenta_sueldosysalarios.clase.nombre == "Resultado":
        debe_sueldosysalarios=abs(cuenta_sueldosysalarios.saldo)
        haber_sueldosysalarios=0        
        print("DEBE: ", debe_sueldosysalarios)
        print("HABER: ", haber_sueldosysalarios)
    else:
        debe_sueldosysalarios=0
        haber_sueldosysalarios=0
        print("DEBE: ", debe_sueldosysalarios)
        print("HABER: ", haber_sueldosysalarios)

    #Mantenimiento de equipo (pasivo) 
    print("\nMantenimiento de equipo: ")
    cuenta_mantenimientodeequipo = Cuenta.objects.get(nombre="Mantenimiento de equipo")  

    if cuenta_mantenimientodeequipo.saldo<0 and cuenta_mantenimientodeequipo.clase.nombre == "Resultado":
        debe_mantenimientodeequipo=0
        haber_mantenimientodeequipo=abs(cuenta_mantenimientodeequipo.saldo)        
        print("DEBE: ", debe_mantenimientodeequipo)
        print("HABER: ", haber_mantenimientodeequipo)
    elif cuenta_mantenimientodeequipo.saldo>0 and cuenta_mantenimientodeequipo.clase.nombre == "Resultado":
        debe_mantenimientodeequipo=abs(cuenta_mantenimientodeequipo.saldo)
        haber_mantenimientodeequipo=0        
        print("DEBE: ", debe_mantenimientodeequipo)
        print("HABER: ", haber_mantenimientodeequipo)
    else:
        debe_mantenimientodeequipo=0
        haber_mantenimientodeequipo=0
        print("DEBE: ", debe_mantenimientodeequipo)
        print("HABER: ", haber_mantenimientodeequipo)

    #Cuentas de resultado acreedoras
    #Ventas (pasivo) 
    print("\nVentas: ")
    cuenta_ventas = Cuenta.objects.get(nombre="Ventas")
    
    if cuenta_ventas.saldo>0 and cuenta_ventas.clase.nombre == "Resultado":
        debe_ventas=abs(cuenta_ventas.saldo)
        haber_ventas=0
        print("DEBE: ", debe_ventas)
        print("HABER: ", haber_ventas)
    elif cuenta_ventas.saldo<0 and cuenta_ventas.clase.nombre == "Resultado":
        debe_ventas=0
        haber_ventas=abs(cuenta_ventas.saldo)
        print("DEBE: ", debe_ventas)
        print("HABER: ", haber_ventas)
    else:
        debe_ventas=0
        haber_ventas=0
        print("DEBE: ", debe_ventas)
        print("HABER: ", haber_ventas)

    #Calculo total activos
    debe_total_activos=debe_ventas+debe_efectivo+debe_bancos+debe_cuentasporcobrar+debe_documentosporcobrar+debe_interesesporcobrar+debe_gastospagadosporadelantado+debe_papeleriayutiles+debe_ivacreditofiscal+debe_ivapagadoporanticipado+debe_insumos+debe_equipoinformatico
    haber_total_activos=haber_ventas+haber_efectivo+haber_bancos+haber_cuentasporcobrar+haber_documentosporcobrar+haber_interesesporcobrar+haber_gastospagadosporadelantado+haber_papeleriayutiles+haber_ivacreditofiscal+haber_ivapagadoporanticipado+haber_insumos+haber_equipoinformatico     

    #Calculo total pasivos + capital
    debe_total_pasivos=debe_cuentasporpagar+debe_prestamosporpagar+debe_prestamosporpagar+debe_otrostitulosvalores+debe_ISSS+debe_AFP+debe_renta+debe_IVA+debe_ivadebitofiscal+debe_interesespercibidos+debe_documentosporpagar+debe_capital
    haber_total_pasivos=haber_cuentasporpagar+haber_prestamosporpagar+haber_prestamosporpagar+haber_otrostitulosvalores+haber_ISSS+haber_AFP+haber_renta+haber_IVA+haber_ivadebitofiscal+haber_interesespercibidos+haber_documentosporpagar+haber_capital

    #Totales generales
    debe_total=debe_total_activos+debe_total_pasivos
    haber_total=haber_total_activos+haber_total_pasivos
    
    #Calculo de las utilidades
    debe_utilidades=debe_ventas+debe_costosporservicios+debe_descuentossobreventas+debe_gastosdeadministracion+debe_sueldosysalarios+debe_mantenimientodeequipo+haber_mantenimientodeequipo
    haber_utilidades=haber_ventas+haber_costosporservicios+haber_descuentossobreventas+haber_gastosdeadministracion+haber_sueldosysalarios+haber_mantenimientodeequipo+haber_mantenimientodeequipo
    
    #Calculo capital social
    debe_capitalsocial=debe_capital+debe_utilidades
    haber_capitalsocial=haber_capital+haber_utilidades

    #Calculo balance general
    debe_balancegeneral=debe_total+debe_capitalsocial-debe_capital
    haber_balancegeneral=haber_total+haber_capitalsocial-haber_capital

    


    return render(request, 'transacciones/hoja_trabajo.html', {
        
        'titulo': titulo,
        #salidas del registro de transacciones
        'form': form, 
        'clases_de_cuentas': clases_de_cuentas, 
        'cuentas': cuentas,

        # ----------sALIDAS PARA EL BALANCE DE COMPROBACION----------------------#
        #Activos
        #Activos corrientes
        'debe_efectivo': debe_efectivo,
        'haber_efectivo': haber_efectivo,
        'debe_bancos': debe_bancos,
        'haber_bancos': haber_bancos,
        'debe_cuentasporcobrar': debe_cuentasporcobrar,
        'haber_cuentasporcobrar': haber_cuentasporcobrar,
        'debe_documentosporcobrar': debe_documentosporcobrar,
        'haber_documentosporcobrar': haber_documentosporcobrar,
        'debe_interesesporcobrar': debe_interesesporcobrar,
        'haber_interesesporcobrar': haber_interesesporcobrar,
        'debe_gastospagadosporadelantado': debe_gastospagadosporadelantado,
        'haber_gastospagadosporadelantado': haber_gastospagadosporadelantado,
        'debe_papeleriayutiles': debe_papeleriayutiles,
        'haber_papeleriayutiles': haber_papeleriayutiles,
        'debe_ivacreditofiscal': debe_ivacreditofiscal,
        'haber_ivacreditofiscal': haber_ivacreditofiscal,
        #Activos no corrientes
        'debe_insumos': debe_insumos,
        'haber_insumos': haber_insumos,
        'debe_equipoinformatico': debe_equipoinformatico,
        'haber_equipoinformatico': haber_equipoinformatico,

        #Pasivos
        'debe_cuentasporpagar': debe_cuentasporpagar,
        'haber_cuentasporpagar': haber_cuentasporpagar,
        'debe_prestamosporpagar': debe_prestamosporpagar,
        'haber_prestamosporpagar': haber_prestamosporpagar,
        'debe_sobregirosbancarios': debe_sobregirosbancarios,
        'haber_sobregirosbancarios': haber_sobregirosbancarios,
        'debe_otrostitulosvalores': debe_otrostitulosvalores,
        'haber_otrostitulosvalores': haber_otrostitulosvalores,
        'debe_ISSS': debe_ISSS,
        'haber_ISSS': haber_ISSS,
        'debe_AFP': debe_AFP,
        'haber_AFP': haber_AFP,
        'debe_renta': debe_renta,
        'haber_renta': haber_renta,
        'debe_IVA': debe_IVA,
        'haber_IVA': haber_IVA,
        'debe_ivadebitofiscal': debe_ivadebitofiscal,
        'haber_ivadebitofiscal': haber_ivadebitofiscal,
        'debe_interesespercibidos': debe_interesespercibidos,
        'haber_interesespercibidos': haber_interesespercibidos,
        'debe_documentosporpagar': debe_documentosporpagar,
        'haber_documentosporpagar': haber_documentosporpagar,

        #Capital
        'debe_capital': debe_capital,
        'haber_capital': haber_capital,

        #Resultados deudoras
        'debe_costosporservicios': debe_costosporservicios,
        'haber_costosporservicios': haber_costosporservicios,
        'debe_descuentossobreventas': debe_descuentossobreventas,
        'haber_descuentossobreventas': haber_descuentossobreventas,
        'debe_gastosdeadministracion': debe_gastosdeadministracion,
        'haber_gastosdeadministracion': haber_gastosdeadministracion,
        'debe_sueldosysalarios': debe_sueldosysalarios,
        'haber_sueldosysalarios': haber_sueldosysalarios,
        'debe_mantenimientodeequipo': debe_mantenimientodeequipo,
        'haber_mantenimientodeequipo': haber_mantenimientodeequipo,

        #Resultados acreedoras
        'debe_ventas': debe_ventas,
        'haber_ventas': haber_ventas,

        #totales
        'debe_total_activos': debe_total_activos,
        'haber_total_activos': haber_total_activos,
        #total pasivos + capital
        'debe_total_pasivos': debe_total_pasivos,
        'haber_total_pasivos': haber_total_pasivos,
        #tatales generales
        'debe_total': debe_total,
        'haber_total': haber_total,


        #--------------------ESTADO DE REUSUTALADO------#
        'debe_utilidades': debe_utilidades,
        'haber_utilidades': haber_utilidades,


        #--------------Estado capital----------------#
        'debe_capitalsocial': debe_capitalsocial,
        'haber_capitalsocial': haber_capitalsocial,

        #---------BAlance genral------------#
        'debe_balancegeneral': debe_balancegeneral,
        'haber_balancegeneral': haber_balancegeneral,
    })



def cierraContable(request):
    return render(request, 'transacciones/cierre_contable.html')    


