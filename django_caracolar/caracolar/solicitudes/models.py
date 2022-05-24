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
    clientx = models.ForeignKey(Clientx, models.CASCADE)
    servicio = models.ForeignKey(ServicioCuidado, models.CASCADE)

    fecha = models.DateField()  # Día de la solicitud del servicio

    # Cambio por anexo de modelo SolicitudCuidadosFechas
    # horaInicio = models.TimeField()                                 # Hora de inicio de la solicitud del servicio
    # horaFin = models.TimeField()                                    # Hora de finalización de la solicitud del servicio

    recurrencia = models.BooleanField()                             # Recurrente SI/NO
    costo = models.FloatField(null=True)
    montoPagado = models.FloatField(null=True)
    medioPago = models.ForeignKey(MedioPago, models.CASCADE)
    estado = models.IntegerField(choices=estados, default= 1)                         # Estados de la solicitud del servicio
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.fecha}: {self.clientx} - {self.servicio}"

    class Meta:
        verbose_name_plural = "Solicitudes de Cuidado"

    def save(self, *args, **kwargs):
        '''
            Se debe analizar el flujo de creación de Movimientos Financieros.
        '''
        self.montoPagado = 22222
        self.costo = 11111
        # import pdb
        # pdb.set_trace()
        # c >> continuar para saltear
        # n >> next
        self.costo = self.servicio.costoReferencia
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
    tiempo = models.IntegerField()          # Tiempo en minutos de la solicitud del servicio (campo calculado)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

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
    tiempo = models.IntegerField()          # Tiempo en minutos de la solicitud del servicio (campo calculado)
    cooperativa = models.ForeignKey(Cooperativa, models.CASCADE)

    def __str__(self):
        return f"{self.solicitud}: {self.dia} - Desde: {self.horaInicio} Hasta: {self.horaFin}"

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


