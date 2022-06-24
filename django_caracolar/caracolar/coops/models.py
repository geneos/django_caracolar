import random
import smtplib
import string
from datetime import date
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib import messages

# Register your models here.

from django.core.checks import messages
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
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
    contraseña = models.CharField('Contraseña',max_length=20)
    host = models.CharField('Email host',max_length=30)
    port = models.IntegerField('Email port')

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

    def verificarEmail(self, cooperativa):
        """Para verificar que toda la informacion necesaria para enviar un mail este completa"""
        if cooperativa.email and cooperativa.contraseña and cooperativa.host and cooperativa.port:
            return True
        return False

    def enviarEmail(self,username,clave):
        """Enviar mail informando la clave y contraseña al cliente"""
        try:
            cooperativa = Cooperativa.objects.get(id=1)
            if not self.verificarEmail(cooperativa):
                return messages.error(self.request,'La cooperativa no tiene la informacion del email completa')
            if not self.email:
                return messages.error(self.request,'El usuario no tiene un mail')
            mailServer = smtplib.SMTP(cooperativa.host,cooperativa.port)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(cooperativa.email, cooperativa.contraseña)
            mensaje = MIMEMultipart()
            mensaje.attach(MIMEText('Hola '+self.nombre+', te compartimos el usuario y la contraseña para acceder a la plataforma caracol.ar \n\n', 'plain'))
            mensaje.attach(MIMEText('Usuario: '+username+'\n', 'plain'))
            mensaje.attach(MIMEText('Contraseña: '+clave+'\n\n', 'plain'))

            #IMAGEN
            body = MIMEText('<p><img src="cid:myimage" /></p>', _subtype='html')
            mensaje.attach(body)
            img_data= open('admin-interface/logo/logo.png', 'rb').read()
            img = MIMEImage(img_data, 'png')
            img.add_header('Content-Id', '<myimage>')
            img.add_header("Content-Disposition", "inline", filename="myimage")
            mensaje.attach(img)
            email = cooperativa.email
            mail_to = self.email
            mensaje['From'] = email
            mensaje['To']= mail_to
            mensaje['Subject'] = "Usuario caracol.ar"
            mailServer.sendmail(email, mail_to, mensaje.as_string())
            return messages.success(self.request, "Email enviado correctamente")
        except Exception as e:
            print("Error en el envio del email")

    def save(self, *args, **kwargs):
        username = self.nombre + '.' + self.apellido
        if not User.objects.filter(username=username).first():
            # clave = StringGenerator("[\l\d]{10}").render_list(3, unique=True)
            chars = string.ascii_uppercase + string.digits
            clave =''.join(random.choice(chars) for _ in range(8))
            user = User.objects.create_user(username, self.email, clave)
            user.save()
            self.usuarix = user
            self.enviarEmail(username, clave)
        self.cooperativa = Cooperativa.objects.first()
        super(Asociadx,self).save(*args, **kwargs)

@receiver(post_delete, sender=Asociadx)
def asociadx_delete_handler(sender, instance, **kwargs):
    """ Cuando se borra un asociado se llama a esta funcion para eliminar su usuario"""
    u = User.objects.get(username = instance.nombre+'.'+instance.apellido)
    u.delete()

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
