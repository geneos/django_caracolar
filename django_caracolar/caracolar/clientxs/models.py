import random
import smtplib
import string
from datetime import date
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.models import User
from django.core.checks import messages
from django.db import models

# Create your models here.
from coops.models import Caracteristica, Cooperativa
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect

from param.models import Ciudad
from strgen import StringGenerator


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

    def verificarEmail(self,cooperativa):
        """Para verificar que toda la informacion necesaria para enviar un mail este completa"""
        if cooperativa.email and cooperativa.contraseña and cooperativa.host and cooperativa.port:
            return True
        return False

    def enviar_email(self,username,clave):
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
        ''' La función save cuando se ejecuta por primera vez crea un usuario para asociarle al cliente.
            Envía los datos de acceso, al correo electrónico del cliente (PENDIENTE).
        '''
        username = self.nombre + '.' + self.apellido
        if not User.objects.filter(username=username).first():
            #clave = StringGenerator("[\l\d]{10}").render_list(3, unique=True)
            chars = string.ascii_uppercase + string.digits
            clave =''.join(random.choice(chars) for _ in range(8))
            user = User.objects.create_user(username, self.email, clave)
            user.save()
            self.usuarix = user
            self.enviar_email(username, clave)
        self.cooperativa = Cooperativa.objects.first()
        super(Clientx,self).save(*args, **kwargs)

@receiver(post_delete, sender=Clientx)
def clientx_delete_handler(sender, instance, **kwargs):
    """ Cuando se borra un cliente se llama a esta funcion para eliminar su usuario"""
    u = User.objects.get(username = instance.nombre+'.'+instance.apellido)
    u.delete()

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

    def save(self, *args, **kwargs):
        self.cooperativa = Cooperativa.objects.first()
        super(CaracteristicaClientx,self).save(*args, **kwargs)
