from django.db import models

# Create your models here.

#Modelos Braian
#Modelo de la clase de cuenta (Braian)
class Clase_Cuenta(models.Model):
    id_clase = models.IntegerField()
    nombre_clase = models.CharField(max_length=30)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ClaseCuenta"
        verbose_name_plural = "ClaseCuentas"

    def __str__(self):
        return self.nombre_clase
    

class Grupo_Cuenta(models.Model):
    id_grupo = models.IntegerField()
    nombre_grupo = models.CharField(max_length=30)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "GrupoCuenta"
        verbose_name_plural = "GrupoCuentas"

    def __str__(self):
        return self.nombre_grupo


class Cuenta_Cuenta(models.Model):
    id_cuenta = models.IntegerField()
    clase_cuenta = models.ForeignKey(Clase_Cuenta, on_delete=models.CASCADE)
    grupo_cuenta = models.ForeignKey(Grupo_Cuenta, on_delete=models.CASCADE)
    nombre_cuenta = models.CharField(max_length=50)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "CuentaCuenta"
        verbose_name_plural = "CuentaCuentas"

    def __str__(self):
        return self.nombre_cuenta