from datetime import date, datetime

from django.db import models

# Create your models here.

from coops.models import Cooperativa, ServicioCuidado, Asociadx
from clientxs.models import Clientx
from param.models import MedioPago

from param.models import Ciudad


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
    tipos = {
        (1, 'Recurrente'),
        (2, 'Por fecha'),
    }
    clientx = models.ForeignKey(Clientx, models.CASCADE)
    servicio = models.ForeignKey(ServicioCuidado, models.CASCADE)
    fecha = models.DateField(default=date.today)  # Día de la solicitud del servicio

    # Cambio por anexo de modelo SolicitudCuidadosFechas
    # horaInicio = models.TimeField()                                 # Hora de inicio de la solicitud del servicio
    # horaFin = models.TimeField()                                    # Hora de finalización de la solicitud del servicio


    tipo= models.IntegerField("Tipo de servicio", choices=tipos)
    costo = models.FloatField("Costo del servicio", null=True, blank=True, help_text='El costo es semanal')
    montoPagado = models.FloatField(default=0)
    medioPago = models.ForeignKey(MedioPago, models.CASCADE)
    estado = models.IntegerField(choices=estados, default= 1)                         # Estados de la solicitud del servicio
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.fecha}: {self.clientx} - {self.servicio}"

    class Meta:
        verbose_name_plural = "Solicitudes de Cuidado"

    def calcular_costo(self):
        if self.tipo== 1:
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


    def save(self, *args, **kwargs):
        self.costo = self.calcular_costo()
        self.cooperativa = Cooperativa.objects.first()
        super(SolicitudCuidados, self).save(*args, **kwargs)



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

    def __str__(self):
        return f"{self.solicitud}: {self.fecha} - Desde: {self.horaInicio} Hasta: {self.horaFin}"

    class Meta:
        verbose_name_plural = "Fechas Solicitudes de Cuidado"


class SolicitudCuidadosAsignacion(models.Model):
    ''' Modelo para representar la asociación de unx asociadx a la prestación de una solicitud de servicio.
        Debido a que puede darse el caso de servicios que lo presten múltiples asociadxs, es una relación NaN.
    '''
    asociadx = models.ForeignKey(Asociadx, models.CASCADE)
    solicitudCuidados = models.ForeignKey(SolicitudCuidados, models.CASCADE)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.asociadx} - {self.solicitudCuidados}"

    class Meta:
        verbose_name_plural = "Asignación de Solicitudes"

    def save(self, *args, **kwargs):
        self.cooperativa = Cooperativa.objects.first()
        super(SolicitudCuidadosAsignacion,self).save(*args, **kwargs)
