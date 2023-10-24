from django.contrib import admin
from .models import ClaseCuenta, Cuenta, Transaccion

# Register your models here.
admin.site.register(ClaseCuenta)
admin.site.register(Cuenta)
admin.site.register(Transaccion)