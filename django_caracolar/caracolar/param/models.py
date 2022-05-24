from django.db import models

# Create your models here.


class Pais(models.Model):
    ''' Modelo para representar paises '''
    nombre = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Paises"


class Provincia(models.Model):
    ''' Modelo para representar provincias '''
    nombre = models.CharField(max_length=200, unique=True)
    pais = models.ForeignKey(Pais, models.CASCADE)

    def __str__(self):
        return f"{self.nombre}, {self.pais}"

    class Meta:
        verbose_name_plural = "Provincias"


class Ciudad(models.Model):
    ''' Modelo para representar ciudades '''
    nombre = models.CharField(max_length=200, unique=True)
    provincia = models.ForeignKey(Provincia, models.CASCADE)

    def __str__(self):
        return f"{self.nombre}, {self.provincia}"

    class Meta:
        verbose_name_plural = "Ciudades"

class MedioPago(models.Model):
    ''' Modelo para representar los medios de pago aceptados en la plataforma.
        A futuro esto nos va a permitir manejar medios de pagos electrónicos.
    '''
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Medios de Pago"
