from django.contrib import admin
from sistema_contable.models import *

# Register your models here.

#Registros (Braian)
class CuentasAdmin(admin.ModelAdmin):
   readonly_fields=("created", "updated")

admin.site.register(Clase_Cuenta)
admin.site.register(Grupo_Cuenta)
admin.site.register(Cuenta_Cuenta)