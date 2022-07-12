import smtplib
from datetime import date, datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib import messages
from django.db import models

# Create your models here.

from coops.models import Cooperativa, ServicioCuidado, Asociadx
from clientxs.models import Clientx
from param.models import MedioPago


class SolicitudCuidados(models.Model):
    ''' Modelo para representar la solicitud de un servicio realizada por unx clientx.
        La solicitud puede ser eventual o recurrente.
        En caso de ser recurrente se asocia con el modelo SolicitudCuidadosRecurrencia.
    '''
    estados = [
        (1, 'Pendiente'),
        (2, 'Asignada'),
        (3, 'Finalizada'),
        (4, 'Cancelada'),
    ]

    tipo = [
        ('Recurrente', 'Recurrente'),
        ('Por fecha', 'Por fecha'),
    ]

    clientx = models.ForeignKey(Clientx, models.CASCADE)
    servicio = models.ForeignKey(ServicioCuidado, models.CASCADE)
    fecha = models.DateField(default=date.today)  # Día de la solicitud del servicio
    infantes= models.IntegerField( default=0, blank=True)
    preadolescentes= models.IntegerField( default=0, blank=True)
    adolecentes = models.IntegerField( default=0, blank=True)
    tipo= models.CharField("Tipo de servico", max_length=17, choices=tipo)
    costo = models.FloatField("Costo del servicio", default=0, blank=True, help_text='El costo es semanal')
    montoPagado = models.FloatField(default=0)
    medioPago = models.ForeignKey(MedioPago, models.CASCADE)
    estado = models.IntegerField(choices=estados, default= 1)                         # Estados de la solicitud del servicio
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def calcular_costo(self):
        if self.tipo== 'Recurrente':
            horarios = SolicitudCuidadosRecurrencia.objects.filter(solicitud=self)
        else:
            horarios = SolicitudCuidadosFechas.objects.filter(solicitud=self)
        hs=0
        min=0
        for h in horarios:
            hs = hs + float(h.tiempo[:2])
            min = min + float(h.tiempo[3:])
        hs = hs + min/60
        return hs*self.servicio.costoReferencia

    def enviar_email(self, host, port, coop_email, coop_contraseña, destinatario, cuerpo, asunto):
        try:
            mail_server = smtplib.SMTP(host, port)
            mail_server.ehlo()
            mail_server.starttls()
            mail_server.ehlo()
            mail_server.login(coop_email, coop_contraseña)
            mensaje = MIMEMultipart()
            mensaje.attach(MIMEText(cuerpo, 'plain'))
            # IMAGEN
            body = MIMEText('<p><img src="cid:myimage" /></p>', _subtype='html')
            mensaje.attach(body)
            img_data = open('admin-interface/logo/logo.png', 'rb').read()
            img = MIMEImage(img_data, 'png')
            img.add_header('Content-Id', '<myimage>')
            img.add_header("Content-Disposition", "inline", filename="myimage")
            mensaje.attach(img)
            email = coop_email
            mensaje['From'] = email
            mensaje['To'] = destinatario
            mensaje['Subject'] = asunto
            mail_server.sendmail(email, destinatario, mensaje.as_string())
        except Exception:
            print('Error al enviar el email')

    def save(self, *args, **kwargs):
        if (self.tipo == ''):
            self.tipo= 'Recurrente'
        self.cooperativa = Cooperativa.objects.first()
        self.costo = self.calcular_costo()
        if self.estado == 1:
            cuerpo = "Hola " + str(self.clientx.nombre) + " se creo la siguiente solicitud:\n\n" + str(self)+"\n\n"
            self.enviar_email(self.cooperativa.host, self.cooperativa.port, self.cooperativa.email, self.cooperativa.contraseña, self.clientx.email, cuerpo,
                     "Creacion de solicitud caracol.ar")
        if self.estado == 4:
            cuerpo = "Hola " + str(self.clientx.nombre) + " se cancelo la siguiente solicitud:\n\n" + str(self)+"\n\n"
            self.enviar_email(self.cooperativa.host, self.cooperativa.port, self.cooperativa.email, self.cooperativa.contraseña, self.clientx.email, cuerpo,
                     "Canclacion de solicitud caracol.ar")

        super(SolicitudCuidados, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.fecha}: {self.clientx} - {self.servicio}"

    class Meta:
        verbose_name = "Solicitud de cuidado recurrente"
        verbose_name_plural = "Solicitudes de cuidado recurrente"

# Proxy de la clase solicitud de cuidados (representa la solicitud por fecha)
class SolicitudCuidadosProxy(SolicitudCuidados):
    class Meta:
            proxy = True
            verbose_name = 'Solicitud de cuidado por fecha'
            verbose_name_plural = 'Solicitud de cuidados por fecha'
    def save(self, *args, **kwargs):
        self.tipo= 'Por fecha'
        super(SolicitudCuidadosProxy, self).save(*args, **kwargs)

class SolicitudCuidadosRecurrencia(models.Model):
    ''' Modelo para representar la recurrencia de una solicitud de un servicio realizada por unx clientx.
        La solicitud puede ser eventual o recurrente.
        En caso de ser recurrente se asocia con el modelo SolicitudCuidadosRecurrencia.
    '''
    dias = [
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miércoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sábado'),
        (7, 'Domingo'),
    ]
    solicitud = models.ForeignKey(SolicitudCuidados, models.CASCADE)
    dia = models.IntegerField(choices=dias, default= 1)    # Día de la solicitud de recurrencia del servicio
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    tiempo = models.CharField(max_length=17,blank=True)          # Tiempo en minutos de la solicitud del servicio (campo calculado)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def segundos_a_segundos_minutos_y_horas(self,segundos): #funcion para guardar hora y minuto hh:mm a partir de la cantidad de segundos
        horas = int(segundos / 60 / 60)
        segundos -= horas*60*60
        minutos = int(segundos/60)
        segundos -= minutos*60
        return f"{horas:02d}:{minutos:02d}"

    def save(self, *args, **kwargs):
        segundos = int((datetime.strptime(str(self.horaFin), '%H:%M:%S')-
        datetime.strptime(str(self.horaInicio), '%H:%M:%S')).seconds)
        self.tiempo= self.segundos_a_segundos_minutos_y_horas(segundos)
        self.cooperativa = Cooperativa.objects.first()
        super(SolicitudCuidadosRecurrencia, self).save(*args, **kwargs)
        SolicitudCuidados.save(self.solicitud)

    def __str__(self):
        return f"{self.solicitud}: {self.dia} - Desde: {self.horaInicio} Hasta: {self.horaFin}"

    class Meta:
        verbose_name_plural = "Recurrencia Solicitudes de Cuidado"



class SolicitudCuidadosFechas(models.Model):
    ''' Modelo para representar las fechas de una solicitud de un servicio realizada por unx clientx.
        La solicitud puede ser eventual o recurrente.
        En caso de ser eventual se asocia con el modelo SolicitudCuidadosFechas.
    '''
    solicitud = models.ForeignKey(SolicitudCuidados, models.CASCADE)
    fecha = models.DateField()    # Fecha de la solicitud del servicio
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    tiempo = models.CharField(max_length=17,blank=True)          # Tiempo en minutos de la solicitud del servicio (campo calculado)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def segundos_a_segundos_minutos_y_horas(self,segundos): #funcion para guardar hora y minuto hh:mm a partir de la cantidad de segundos
        horas = int(segundos / 60 / 60)
        segundos -= horas*60*60
        minutos = int(segundos/60)
        segundos -= minutos*60
        return f"{horas:02d}:{minutos:02d}"

    def save(self, *args, **kwargs):
            segundos = int((datetime.strptime(str(self.horaFin), '%H:%M:%S')-
			datetime.strptime(str(self.horaInicio), '%H:%M:%S')).seconds)
            self.tiempo= self.segundos_a_segundos_minutos_y_horas(segundos)
            self.cooperativa = Cooperativa.objects.first()
            super(SolicitudCuidadosFechas, self).save(*args, **kwargs)
            SolicitudCuidados.save(self.solicitud)

    def __str__(self):
        return f"{self.solicitud}: {self.fecha} - Desde: {self.horaInicio} Hasta: {self.horaFin}"

    class Meta:
        verbose_name_plural = "Fechas Solicitudes de Cuidado"


class SolicitudCuidadosAsignacion(models.Model):
    ''' Modelo para representar la asociación de unx asociadx a la prestación de una solicitud de servicio.
        Debido a que puede darse el caso de servicios que lo presten múltiples asociadxs, es una relación NaN.
    '''
    asociadx = models.ForeignKey(Asociadx, models.CASCADE)
    solicitudCuidados = models.ForeignKey(SolicitudCuidados, models.CASCADE, limit_choices_to={'estado': 1})
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.asociadx} - {self.solicitudCuidados}"

    class Meta:
        verbose_name_plural = "Asignación de Solicitudes"

    def verificar_email(self, cooperativa):
        """Para verificar que toda la informacion necesaria para enviar un mail este completa"""
        if cooperativa.email and cooperativa.contraseña and cooperativa.host and cooperativa.port:
            return True
        return False

    def enviar_email(self, host, port, coop_email, coop_contraseña, destinatario, cuerpo, asunto):
        mail_server = smtplib.SMTP(host, port)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(coop_email, coop_contraseña)
        mensaje = MIMEMultipart()
        mensaje.attach(MIMEText(cuerpo, 'plain'))
        # IMAGEN
        body = MIMEText('<p><img src="cid:myimage" /></p>', _subtype='html')
        mensaje.attach(body)
        img_data = open('admin-interface/logo/logo.png', 'rb').read()
        img = MIMEImage(img_data, 'png')
        img.add_header('Content-Id', '<myimage>')
        img.add_header("Content-Disposition", "inline", filename="myimage")
        mensaje.attach(img)
        email = coop_email
        mensaje['From'] = email
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto
        mail_server.sendmail(email, destinatario, mensaje.as_string())

    def enviar_emails(self):
        try:
            cooperativa = Cooperativa.objects.get(id=1)
            a = str(self.asociadx).split()
            mail_to_asociadx = Asociadx.objects.get(cuit=a[0]).email
            clientx = self.solicitudCuidados.clientx
            if not self.verificar_email(cooperativa):
                return messages.error(self.request, 'La cooperativa no tiene la informacion del email completa')
            if not mail_to_asociadx:
                return messages.error(self.request, 'El usuario no tiene un mail')
            self.enviar_email(cooperativa.host, cooperativa.port, cooperativa.email, cooperativa.contraseña, mail_to_asociadx, 'Hola '+str(self.asociadx).split()[-1]+', tenes asignada la siguiente solicitud:\n\n'+str(self.solicitudCuidados)+'\n\n', "Asignacion caracol.ar")
            self.enviar_email(cooperativa.host, cooperativa.port, cooperativa.email, cooperativa.contraseña, clientx.email, 'Hola '+str(clientx.nombre)+', se asigno la solicitud:\n\n'+str(self.solicitudCuidados)+'\n\n al asociadx: \n\n'+str(self.asociadx.nombre)+' '+str(self.asociadx.apellido)+'\n\n', "Asignacion de solicitud caracol.ar")
            return messages.success(self.request, "Email enviado correctamente")
        except Exception:
            print("Error en el envio del email")

    def save(self, *args, **kwargs):
        self.cooperativa = Cooperativa.objects.first()
        self.solicitudCuidados.estado = 2
        SolicitudCuidados.save(self.solicitudCuidados)
        self.enviar_emails()
        super(SolicitudCuidadosAsignacion, self).save(*args, **kwargs)
