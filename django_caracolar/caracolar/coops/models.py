import random
import string
from datetime import date

from django.db import models
from param.models import Ciudad
from django.contrib.auth.models import User

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
    ciudad = models.ForeignKey(Ciudad, models.CASCADE,null=True)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.matricula},{self.razon_social}"

    class Meta:
        verbose_name_plural = "Cooperativas"

class TipoServicio(models.Model):
    ''' Modelo para representar tipos de servicios de cuidados '''
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=200, unique=True, blank=True, null= True)
    icono = models.CharField(max_length=200, unique=True, blank=True, null= True)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Tipos de Servicios"

    def save(self, *args, **kwargs):
        self.cooperativa = Cooperativa.objects.first()
        super(TipoServicio,self).save(*args, **kwargs)

class ServicioCuidado(models.Model):
    ''' Modelo para representar servicios de cuidados '''
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=200, unique=True, blank=True, null= True)
    icono = models.CharField(max_length=200, unique=True, blank=True, null= True)
    tipo = models.ForeignKey(TipoServicio, models.CASCADE)
    costoReferencia = models.FloatField()
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.nombre}, {self.tipo}"

    class Meta:
        verbose_name_plural = "Servicios de Cuidado"

    def save(self, *args, **kwargs):
        self.cooperativa = Cooperativa.objects.first()
        super(ServicioCuidado,self).save(*args, **kwargs)


class CaracteristicaCuidado(models.Model):
    ''' Modelo para representar caractyerísticas de los servicios de cuidados '''
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=200, unique=True, blank=True, null= True)
    icono = models.CharField(max_length=200, unique=True, blank=True, null= True)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Características de Cuidado"

    def save(self, *args, **kwargs):
        self.cooperativa = Cooperativa.objects.first()
        super(CaracteristicaCuidado,self).save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        self.cooperativa = Cooperativa.objects.first()
        super(ServicioCaracteristicaCuidado,self).save(*args, **kwargs)

class Asociadx(models.Model):
    ''' Modelo para representar lxs asociadxs (prestadorxs de servicios) a una cooperativa '''
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    cuit = models.CharField("Cuil/Cuit", max_length=11, unique=True)
    direccion = models.CharField(max_length=100,  blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, models.CASCADE)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)
    ingreso = models.DateField("Fecha de ingreso", default=date.today)
    usuarix = models.ForeignKey(User, models.CASCADE, blank=True)

    def __str__(self):
        return f"{self.cuit} - {self.apellido}, {self.nombre}"

    class Meta:
        verbose_name_plural = "Asociadxs"

    def save(self, *args, **kwargs):
        username = self.nombre + '.' + self.apellido
        if not User.objects.filter(username=username).first():
            # clave = StringGenerator("[\l\d]{10}").render_list(3, unique=True)
            chars = string.ascii_uppercase + string.digits
            clave =''.join(random.choice(chars) for _ in range(8))
            user = User.objects.create_user(username, self.email, clave)
            user.save()
            self.usuarix = user
        #falta el mail
        self.cooperativa = Cooperativa.objects.first()
        super(Asociadx,self).save(*args, **kwargs)


class Caracteristica(models.Model):
    ''' Modelo para representar características de lxs asociadxs '''
    nombre = models.CharField(max_length=200, unique=True)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Características de Asociadx"

    def save(self, *args, **kwargs):
        self.cooperativa = Cooperativa.objects.first()
        super(Caracteristica,self).save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        self.cooperativa = Cooperativa.objects.first()
        super(CaracteristicaAsociadxs,self).save(*args, **kwargs)
