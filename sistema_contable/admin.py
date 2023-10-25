from django.contrib import admin
from sistema_contable.models import *

# Register your models here.

#Registros (Braian)
class CuentasAdmin(admin.ModelAdmin):
   readonly_fields=("created", "updated")

admin.site.register(ClaseCuenta)
admin.site.register(Cuenta)
admin.site.register(Transaccion)