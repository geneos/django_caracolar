from django.db import models
from param.models import Ciudad

# Create your models here.
class Cooperativa(models.Model):
    ''' Modelo para representar cooperativas
        Algunos modelos van a estar asociados al este modelo,
        para representar un agrupamiento y segmentación por cooperativa.
    '''
    razon_social = models.CharField(max_length=200, unique=True)
    matricula = models.CharField(max_length=200, unique=True)
    cuit = models.CharField(max_length=11, unique=True)
    direccion = models.CharField(max_length=100)
    ciudad = models.ForeignKey(Ciudad, models.CASCADE)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.matricula},{self.razon_social}"

    class Meta:
        verbose_name_plural = "Cooperativas"

class TipoServicio(models.Model):
    ''' Modelo para representar tipos de servicios de cuidados '''
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=200, unique=True)
    icono = models.CharField(max_length=200, unique=True)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Tipos de Servicios"


class ServicioCuidado(models.Model):
    ''' Modelo para representar servicios de cuidados '''
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=200, unique=True)
    icono = models.CharField(max_length=200, unique=True)
    tipo = models.ForeignKey(TipoServicio, models.CASCADE)
    costoReferencia = models.FloatField()
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.nombre}, {self.tipo}"

    class Meta:
        verbose_name_plural = "Servicios de Cuidado"


class CaracteristicaCuidado(models.Model):
    ''' Modelo para representar caractyerísticas de los servicios de cuidados '''
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=200, unique=True)
    icono = models.CharField(max_length=200, unique=True)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Características de Cuidado"


class ServicioCaracteristicaCuidado(models.Model):
    ''' Modelo para representar la relación de una característica con un servicio de cuidados.
        Esta relación puede ser NaN.
    '''
    servicio = models.ForeignKey(ServicioCuidado, models.CASCADE)
    caracteristica = models.ForeignKey(CaracteristicaCuidado, models.CASCADE)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.servicio} - {self.caracteristica}"

    class Meta:
        verbose_name_plural = "Características de Servicios de Cuidado"

class Asociadx(models.Model):
    ''' Modelo para representar lxs asociadxs (prestadorxs de servicios) a una cooperativa '''
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    cuit = models.CharField(max_length=11, unique=True)
    direccion = models.CharField(max_length=100)
    ciudad = models.ForeignKey(Ciudad, models.CASCADE)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)
    ingreso = models.DateField()

    def __str__(self):
        return f"{self.cuit} - {self.apellido}, {self.nombre}"

    class Meta:
        verbose_name_plural = "Asociadxs"


class Caracteristica(models.Model):
    ''' Modelo para representar características de lxs asociadxs '''
    nombre = models.CharField(max_length=200, unique=True)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Características de Asociadx"


class CaracteristicaAsociadxs(models.Model):
    ''' Modelo para representar la relación de una característica con un asociadx.
        Esta relación puede ser NaN.
    '''
    asociadx = models.ForeignKey(Asociadx, models.CASCADE)
    caracteristica = models.ForeignKey(Caracteristica, models.CASCADE)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.asociadx} - {self.caracteristica}"

    class Meta:
        verbose_name_plural = "Asignación de Características de Asociadx"