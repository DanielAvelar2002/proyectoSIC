# forms.py

from django import forms
from .models import Transaccion, ClaseCuenta, Cuenta

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['fecha', 'concepto', 'monto', 'iva', 'cargo_clase', 'cargo_cuenta', 'abono_clase', 'abono_cuenta']

