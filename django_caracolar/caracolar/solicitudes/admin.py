import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib import admin, messages
from django.contrib.admin.helpers import ActionForm
from django import forms
from .form import ControlFechaRecurrenciaForm, ControlFechaFechasForm
from .models import SolicitudCuidadosRecurrencia, SolicitudCuidadosFechas, SolicitudCuidados, SolicitudCuidadosProxy, \
    SolicitudCuidadosAsignacion
from coops.models import Cooperativa


class SolicitudCuidadosRecurrenteTabularInline(admin.TabularInline):
    model = SolicitudCuidadosRecurrencia
    readonly_fields = ['tiempo', 'cooperativa']  # el tiempo no se puede editar porque se calcula solo
    can_delete = True
    form = ControlFechaRecurrenciaForm


class SolicitudCuidadosFechasTabularInline(admin.TabularInline):
    model = SolicitudCuidadosFechas
    readonly_fields = ['tiempo', 'cooperativa']
    can_delete = True
    form = ControlFechaFechasForm


class UpdateActionForm(ActionForm):
    monto = forms.IntegerField()


# Acciones para cambiar de estado
# @admin.action(description='Asignar solicutid')
# def asignar(self, request, queryset):
#    queryset.update(estado=2)
#    messages.success(request, "Estado Actualizado correctamente")


def enviar_email(host, port, coop_email, coop_contraseña, destinatario, cuerpo, asunto):
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


@admin.action(description='Finalizar solicitud')
def finalizar(modeladmin, request, queryset):
    queryset.update(estado=3)
    cooperativa = Cooperativa.objects.get(id=1)
    cliente = queryset[0].clientx
    cuerpo = "Hola " + str(cliente.nombre) + " la siguiente solicitud se encuentra finalizada:\n\n" + str(queryset[0])
    enviar_email(cooperativa.host, cooperativa.port, cooperativa.email, cooperativa.contraseña, cliente.email, cuerpo,
                 "Solicitud finalizada caracol.ar")
    messages.success(request, "Estado Actualizado correctamente")


@admin.action(description='Cancelar solicitud')
def cancelar(modeladmin, request, queryset):
    queryset.update(estado=4)
    cooperativa = Cooperativa.objects.get(id=1)
    cliente = queryset[0].clientx
    cuerpo = "Hola " + str(cliente.nombre) + " la siguiente solicitud se cancelo:\n\n" + str(queryset[0])
    enviar_email(cooperativa.host, cooperativa.port, cooperativa.email, cooperativa.contraseña, cliente.email, cuerpo,
                 "Solicitud cancelada caracol.ar")
    messages.success(request, "Estado Actualizado correctamente")


@admin.action(description="Registrar Pago")
def registrarPago(self, request, queryset):
    monto_str = request.POST['monto']
    print("Monto " + monto_str)
    monto = float(monto_str)
    queryset.update(montoPagado=monto)
    messages.success(request, "Monto Pagado Actualizado correctamente")


# Administrador Solicitud de cuidados
class SolicitudCuidadosAdmin(admin.ModelAdmin):
    icon_name = 'gamepad'
    # action_form = UpdateActionForm
    actions = [finalizar, cancelar]  # ,asignar]#, registrarPago]
    inlines = [SolicitudCuidadosRecurrenteTabularInline]  # , SolicitudCuidadosFechasTabularInline]
    list_display = ['fecha', 'clientx', 'servicio', 'estado']
    readonly_fields = ['fecha', 'montoPagado', 'estado', 'costo', 'cooperativa', 'tipo']

    def get_queryset(self, request):
        return super(SolicitudCuidadosAdmin, self).get_queryset(request).filter(tipo='Recurrente')

    def queryset(self, request):
        return (super(SolicitudCuidadosAdmin, self).queryset(request).filter(tipo='Recurrente', is_active=True))


class SolicitudCuidadosAdminProxy(admin.ModelAdmin):
    icon_name = 'gamepad'
    # action_form = UpdateActionForm
    actions = [finalizar, cancelar]  # ,asignar, registrarPago]
    inlines = [SolicitudCuidadosFechasTabularInline]
    list_display = ['fecha', 'clientx', 'servicio', 'estado']
    readonly_fields = ['fecha', 'montoPagado', 'estado', 'costo', 'cooperativa', 'tipo']

    def get_queryset(self, request):
        return super(SolicitudCuidadosAdminProxy, self).get_queryset(request).filter(tipo='Por fecha')

    def queryset(self, request):
        return (super(SolicitudCuidadosAdminProxy, self).queryset(request).filter(tipo='Por fecha', is_active=True))


class SolicitudCuidadosAsignacionAdmin(admin.ModelAdmin):
    list_display = ['asociadx', 'solicitudCuidados']
    readonly_fields = ['cooperativa']


admin.site.register(SolicitudCuidados, SolicitudCuidadosAdmin)
admin.site.register(SolicitudCuidadosProxy, SolicitudCuidadosAdminProxy)
admin.site.register(SolicitudCuidadosAsignacion, SolicitudCuidadosAsignacionAdmin)
