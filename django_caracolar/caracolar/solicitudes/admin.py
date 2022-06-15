from django.contrib import admin, messages

# Register your models here.
from django.contrib.admin.helpers import ActionForm
from django import forms
from django.http import HttpResponse
#from lxml.html.builder import HTML
from django.shortcuts import render
from django.db import models

from .models import SolicitudCuidadosRecurrencia, SolicitudCuidadosFechas, SolicitudCuidados, SolicitudCuidadosProxy, \
    SolicitudCuidadosAsignacion


class SolicitudCuidadosRecurrenteTabularInline(admin.TabularInline):
    model = SolicitudCuidadosRecurrencia
    readonly_fields = ['tiempo', 'cooperativa'] #el tiempo no se puede editar porque se calcula solo
    can_delete = True

class SolicitudCuidadosFechasTabularInline(admin.TabularInline):
    model = SolicitudCuidadosFechas
    readonly_fields = ['tiempo', 'cooperativa']
    can_delete = True


class UpdateActionForm(ActionForm):
	monto = forms.IntegerField()

#Acciones para cambiar de estado
@admin.action(description='Asignar solicutid')
def asignar(self, request, queryset):
    queryset.update(estado=2)
    messages.success(request, "Estado Actualizado correctamente")

@admin.action(description='Finalizar solicitud')
def finalizar(modeladmin, request, queryset):
    queryset.update(estado=3)
    messages.success(request, "Estado Actualizado correctamente")

@admin.action(description= 'Cancelar solicitud')
def cancelar(modeladmin, request, queryset):
    queryset.update(estado=4)
    messages.success(request, "Estado Actualizado correctamente")

@admin.action(description="Registrar Pago")
def registrarPago(self, request, queryset):
    monto_str = request.POST['monto']
    print("Monto " + monto_str)
    monto = float(monto_str)
    queryset.update(montoPagado=monto)
    messages.success(request, "Monto Pagado Actualizado correctamente")


#Administrador Solicitud de cuidados
class SolicitudCuidadosAdmin(admin.ModelAdmin):
    icon_name = 'gamepad'
   # action_form = UpdateActionForm
    actions= [asignar, finalizar, cancelar]#, registrarPago]
    inlines = [SolicitudCuidadosRecurrenteTabularInline]#, SolicitudCuidadosFechasTabularInline]
    list_display = ['fecha', 'clientx', 'servicio', 'estado']
    readonly_fields= ['fecha', 'montoPagado', 'estado', 'costo', 'cooperativa', 'tipo']
    def get_queryset(self,request):
        return super(SolicitudCuidadosAdmin, self).get_queryset(request).filter(tipo='Recurrente')
    def queryset(self, request):
        return (super(SolicitudCuidadosAdmin, self).queryset(request).filter(tipo='Recurrente', is_active=True))

class SolicitudCuidadosAdminProxy(admin.ModelAdmin):
    icon_name = 'gamepad'
   # action_form = UpdateActionForm
    actions= [asignar, finalizar, cancelar]#, registrarPago]
    inlines = [SolicitudCuidadosFechasTabularInline]
    list_display = ['fecha', 'clientx', 'servicio', 'estado']
    readonly_fields= ['fecha', 'montoPagado', 'estado', 'costo', 'cooperativa', 'tipo']
    def get_queryset(self,request):
        return super(SolicitudCuidadosAdminProxy, self).get_queryset(request).filter(tipo='Por fecha')
    def queryset(self, request):
        return (super(SolicitudCuidadosAdminProxy, self).queryset(request).filter(tipo='Por fecha', is_active=True))


class SolicitudCuidadosAsignacionAdmin(admin.ModelAdmin):
    list_display= ['asociadx', 'solicitudCuidados']
    readonly_fields= ['cooperativa']



admin.site.register(SolicitudCuidados,SolicitudCuidadosAdmin)
admin.site.register(SolicitudCuidadosProxy,SolicitudCuidadosAdminProxy)
admin.site.register(SolicitudCuidadosAsignacion,SolicitudCuidadosAsignacionAdmin)
