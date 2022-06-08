import random
import string
from datetime import date

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from coops.models import Caracteristica, Cooperativa

from param.models import Ciudad


class Clientx(models.Model):
    ''' Modelo para representar lxs clientxs que pueden solicitar servicios en la plataforma '''
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    cuit = models.CharField("Cuit/Cuil", max_length=11, unique=True, null=True, blank=True)
    direccion = models.CharField(max_length=100)
    ciudad = models.ForeignKey(Ciudad, models.CASCADE)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    ingreso = models.DateField("Fecha de ingreso", default=date.today)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)
    usuarix = models.ForeignKey(User, models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.cuit} - {self.apellido}, {self.nombre}"

    class Meta:
        verbose_name_plural = "Clientxs"

    def save(self, *args, **kwargs):
        ''' La función save cuando se ejecuta por primera vez crea un usuario para asociarle al cliente.
            Envía los datos de acceso, al correo electrónico del cliente (PENDIENTE).
        '''
        username = self.nombre + '.' + self.apellido
        if not User.objects.filter(username=username).first():
            # clave = StringGenerator("[\l\d]{10}").render_list(3, unique=True)
            chars = string.ascii_uppercase + string.digits
            clave =''.join(random.choice(chars) for _ in range(8))
            user = User.objects.create_user(username, self.email, clave)
            user.save()
            self.usuarix = user
            #falta mandar mail
        super(Clientx,self).save(*args, **kwargs)

class CaracteristicaClientx(models.Model):
    ''' Modelo para representar la relación de una característica con unx clientx.
        La asociación, es con el mismo padrón de carcacterísticas que se relacionan a lxs asociadxs,
        para poder emparentarlxs en desarrollos futuros.
        Esta relación puede ser NaN.
    '''
    clientx = models.ForeignKey(Clientx, models.CASCADE)
    caracteristica = models.ForeignKey(Caracteristica, models.CASCADE)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.clientx} - {self.caracteristica}"
    class Meta:
        verbose_name_plural = "Características de Clientxs"

