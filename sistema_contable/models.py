from django.db import models
from decimal import Decimal


# Create your models here.
class ClaseCuenta(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Cuenta(models.Model):
    codigoCA = models.CharField(max_length=10, default='ValorPredeterminado')
    nombre = models.CharField(max_length=100)
    clase = models.ForeignKey(ClaseCuenta, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        #return self.nombre
        return f"{self.nombre} ({self.clase.nombre}) ({self.saldo})"
    
class Transaccion(models.Model):
    fecha = models.DateField()
    concepto = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Campo para el tipo de IVA
    IVA_CHOICES = [
        ('CreditoFiscal', 'IVA Crédito Fiscal'),
        ('DebitoFiscal', 'IVA Débito Fiscal'),
        ('Ninguno', 'Ninguno'),
    ]
    iva = models.CharField(max_length=15, choices=IVA_CHOICES, default='Ninguno')
   

    cargo_clase = models.ForeignKey(ClaseCuenta, related_name='cargos', on_delete=models.CASCADE)
    cargo_cuenta = models.ForeignKey(Cuenta, related_name='cargos', on_delete=models.CASCADE)
    abono_clase = models.ForeignKey(ClaseCuenta, related_name='abonos', on_delete=models.CASCADE)
    abono_cuenta = models.ForeignKey(Cuenta, related_name='abonos', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.concepto} ({self.monto})"
    
    #validaciones dentro del user admin
    def save(self, *args, **kwargs):
        if self.cargo_clase and not self.cargo_cuenta.clase == self.cargo_clase:
            raise ValueError("La cuenta de cargo no pertenece a la clase seleccionada.")
        if self.abono_clase and not self.abono_cuenta.clase == self.abono_clase:
            raise ValueError("La cuenta de abono no pertenece a la clase seleccionada.")
        super(Transaccion, self).save(*args, **kwargs)

    def clean(self):
        if self.monto < 0:
            raise ValidationError("El monto no puede ser negativo.")

        if self.cargo_cuenta.clase != self.cargo_clase:
            raise ValidationError("La cuenta de cargo no pertenece a la clase seleccionada.")

        if self.abono_cuenta.clase != self.abono_clase:
            raise ValidationError("La cuenta de abono no pertenece a la clase seleccionada.")

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"

    def save(self, *args, **kwargs):
        

        #Si selecciona Iva credito fiscal
        if self.iva == 'CreditoFiscal':
            # Actualiza el saldo de la cuenta de abono
            self.abono_cuenta.saldo += self.monto
            self.abono_cuenta.save()    

            # Calcula el IVA
            iva_amount = Decimal('0.13') * self.monto
            self.monto += iva_amount
            # Agrega el IVA a la cuenta de IVA Crédito Fiscal en el haber
            iva_cuenta = Cuenta.objects.get(nombre='Iva credito fiscal')
            iva_cuenta.saldo += iva_amount
            iva_cuenta.save()
            
            # Actualiza el saldo de la cuenta de cargo
            self.cargo_cuenta.saldo -= self.monto
            self.cargo_cuenta.save()

        #Si selecciona Iva debito fiscal
        elif self.iva == 'DebitoFiscal':
            # Actualiza el saldo de la cuenta de cargo
            self.cargo_cuenta.saldo -= self.monto
            self.cargo_cuenta.save()

            iva_amount = Decimal('0.13') * self.monto
            self.monto += iva_amount
            # Agrega el IVA a la cuenta de IVA Debito Fiscal en el haber
            iva_cuenta = Cuenta.objects.get(nombre='Iva debito fiscal')
            iva_cuenta.saldo += iva_amount
            iva_cuenta.save()

            # Actualiza el saldo de la cuenta de abono
            self.abono_cuenta.saldo += self.monto
            self.abono_cuenta.save()  

        #Si selecciona Ninguna
        elif self.iva=='Ninguno':
            # Actualiza el saldo de la cuenta de abono
            self.abono_cuenta.saldo += self.monto
            self.abono_cuenta.save()  

             # Actualiza el saldo de la cuenta de cargo
            self.cargo_cuenta.saldo -= self.monto
            self.cargo_cuenta.save()                  

        super(Transaccion, self).save(*args, **kwargs)





