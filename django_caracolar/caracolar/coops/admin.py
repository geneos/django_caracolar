import os
from datetime import datetime, date
from io import BytesIO

import datetime as datetime
from django.contrib import admin, messages
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas

from .form import fechasForm
from .models import Cooperativa, TipoServicio, ServicioCuidado, CaracteristicaCuidado, ServicioCaracteristicaCuidado, \
    Asociadx, CaracteristicaAsociadxs, Caracteristica

# Register your models here.
from solicitudes.models import SolicitudCuidadosAsignacion, SolicitudCuidados, SolicitudCuidadosFechas, \
    SolicitudCuidadosRecurrencia


class ServicioCaracteristicaCuidadoInline(admin.TabularInline):
    model = ServicioCaracteristicaCuidado
    can_delete = True
    readonly_fields = ['cooperativa']

class ServicioCuidadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'costoReferencia')
    search_fields = ('nombre', 'descripcion')
    inlines = [ServicioCaracteristicaCuidadoInline]
    readonly_fields = ['cooperativa']


class AsociadxTabularInline(admin.TabularInline):
    model = Asociadx
    can_delete = False
    readonly_fields = ['cooperativa']

    def has_add_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False


class CaracteristicaAsociadxsTabularInline(admin.TabularInline):
    model = CaracteristicaAsociadxs
    can_delete = True
    readonly_fields = ['cooperativa']

    # def has_add_permission(self, request, obj=None):
    #     return False
    #
    # def has_edit_permission(self, request, obj=None):
    #     return False

class CaracteristicaCuidadoAdmin(admin.ModelAdmin):
    readonly_fields = ['cooperativa']

class ServicioCaracteristicaCuidadoAdmin(admin.ModelAdmin):
     readonly_fields = ['cooperativa']

def cabeceraTablaServiciosRecurrente(pdf,y):
    pdf.setFont("Helvetica-Bold", 10)
    xlist = [45, 132, 217, 329, 468]
    ylist = [y, y-18]
    pdf.drawString(47, y-16, 'Dia')
    pdf.drawString(135, y-16, 'Hora Inicio')
    pdf.drawString(220, y-16, 'Hora Fin')
    pdf.drawString(332, y-16, 'Cantidad de horas')
    pdf.grid(xlist, ylist)

def cabeceraTablaServiciosFecha(pdf,y):
    pdf.setFont("Helvetica-Bold", 10)
    xlist = [45, 132, 217, 329, 468]
    ylist = [y, y-18]
    pdf.drawString(47, y-16, 'Fecha')
    pdf.drawString(135, y-16, 'Hora Inicio')
    pdf.drawString(220, y-16, 'Hora Fin')
    pdf.drawString(332, y-16, 'Cantidad de horas')
    pdf.grid(xlist, ylist)


def infoAsociadx(pdf,x,y,d):
    pdf.drawString(x, y, 'Nombre y Apellido: '+str(d.nombre) + " " + str(d.apellido))
    y=y-15
    pdf.drawString(x, y, 'Cuit/Cuil: '+str(d.cuit))
    y=y-15
    pdf.drawString(x, y, 'Direccion: '+str(d.direccion))
    y=y-15
    pdf.drawString(x, y, 'Ciudad: '+str(d.ciudad))
    y=y-15
    pdf.drawString(x, y, 'Telefono: '+str(d.telefono))
    y=y-15
    pdf.drawString(x, y, 'Email: '+str(d.email))
    y=y-15
    pdf.drawString(x, y, 'Cooperativa: '+str(d.cooperativa))
    y=y-15
    pdf.drawString(x, y, 'Fecha de ingreso: '+str(d.ingreso))
    y = y-30
    return y

def infoServicioRecurrente(pdf,x,y,s):
    pdf.drawString(x, y+1, 'Servicio recurrentes')
    solicitudRecurrente= SolicitudCuidadosRecurrencia.objects.filter(solicitud= s.id)
    y=y-2
    if (y<30):
            y = 800
            pdf.showPage()
            y = y-18
    cabeceraTablaServiciosRecurrente(pdf,y)
    pdf.setFont("Helvetica", 10)
    y=y-18
    for sr in solicitudRecurrente:
        xlist = [45, 132, 217, 329, 468]
        ylist = [y, y-18]
        pdf.grid(xlist, ylist)
        if sr.dia == 1:
            pdf.drawString(48, y-16, "Lunes")
        if sr.dia == 2:
            pdf.drawString(48, y-16, "Martes")
        if sr.dia == 3:
            pdf.drawString(48, y-16, "Miercoles")
        if sr.dia == 4:
            pdf.drawString(48, y-16, "Jueves")
        if sr.dia == 5:
            pdf.drawString(48, y-16, "Viernes")
        if sr.dia == 6:
            pdf.drawString(48, y-16, "Sabado")
        if sr.dia == 7:
            pdf.drawString(48, y-16, "Domingo")
        pdf.drawString(135, y-16,str(sr.horaInicio))
        pdf.drawString(220, y-16,str(sr.horaFin))
        pdf.drawString(332, y-16,str(sr.tiempo))
        y = y-18
        if (y<30):
            y = 800
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            cabeceraTablaServiciosRecurrente(pdf,y)
            pdf.setFont("Helvetica", 10)
            y = y-18
    return y

def generarInformeAsociadx(pdf,request,queryset):
    settings_dir = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    img = os.path.join(PROJECT_ROOT, 'admin-interface/logo/photo4976484941684648281.png')
    pdf.drawImage(img, 22,720,550,100)
    asociados = queryset.all()
    y = 700
    x = 45
    e = 15
    pdf.setFont("Helvetica", 12)
    pdf.drawString(x, y, 'INFORME DEL ASOCIADO')
    pdf.setFont("Helvetica", 10)
    y= y-15
    if asociados.count()>1:
        return messages.error(request,'Debe seleccionar solo un asociado')
    else:
        for a in asociados:
            y= infoAsociadx(pdf, x, y,a)
            caracterisicas = CaracteristicaAsociadxs.objects.filter(asociadx = a.id)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(x, y, 'Caracteristicas del asociado:')
            for c in caracterisicas:
                y= y-15
                pdf.drawString(x, y, '- '+str(c.caracteristica.nombre))
            solicitudAsignada = SolicitudCuidadosAsignacion.objects.filter(asociadx = a.id)
            for sa in solicitudAsignada:
                y=y-15
                solicitudCuidado= SolicitudCuidados.objects.filter(id = sa.solicitudCuidados.id)
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(x, y, 'Servicios asignados:')
                pdf.setFont("Helvetica-Bold", 10)
                y= y-15
                for s in solicitudCuidado:
                    y = y-15
                    pdf.setFont("Helvetica-Bold", 10)
                    pdf.drawString(x, y, 'Servicio: '+str(s.servicio.nombre))
                    y=y-15
                    pdf.drawString(x, y, 'Costo referencial: '+str(s.servicio.costoReferencia))
                    y=y-15
                    pdf.drawString(x, y, 'Cooperativa: '+str(s.servicio.cooperativa))
                    y=y-15
                    if s.estado == 2:
                        pdf.drawString(x, y, 'Estado: Asignada')
                    if s.estado == 3:
                        pdf.drawString(x, y, 'Estado: Finalizada')
                    if s.estado == 4:
                        pdf.drawString(x, y, 'Estado: Cancelada')
                    y=y-18
                    pdf.setFont("Helvetica", 10)
                    if s.tipo == 2:
                        if (y<30):
                            y = 800
                            pdf.showPage()
                            y = y-18
                        pdf.drawString(x, y+1, 'Servicios por fecha')
                        solicitudFecha= SolicitudCuidadosFechas.objects.filter(solicitud= s.id)
                        y=y-2
                        cabeceraTablaServiciosFecha(pdf,y)
                        pdf.setFont("Helvetica", 10)
                        y=y-18
                        for sr in solicitudFecha:
                            xlist = [45, 132, 217, 329, 468]
                            ylist = [y, y-18]
                            pdf.grid(xlist, ylist)
                            pdf.drawString(48, y-16, str(sr.fecha))
                            pdf.drawString(135, y-16,str(sr.horaInicio))
                            pdf.drawString(220, y-16,str(sr.horaFin))
                            pdf.drawString(332, y-16,str(sr.tiempo))
                            y = y-18
                            if (y<50):
                                y = 800
                                pdf.showPage()
                                cabeceraTablaServiciosFecha(pdf,y)
                                pdf.setFont("Helvetica", 10)
                                y = y-18
                    else:
                        y= infoServicioRecurrente(pdf,x,y,s)
                        y= y-20
            pdf.showPage()
            pdf.save()


def emitirInformeAsociadx(self, request, queryset):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        generarInformeAsociadx(pdf,request,queryset)
        buffer.seek(0)
        messages.success(request, "Informe emitido")
        return FileResponse(buffer, as_attachment=True, filename='Informe cliente.pdf')


class AsociadxAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'ciudad', 'ingreso')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter= ('ciudad',)
    actions = [emitirInformeAsociadx]
    # inlines = [CaracteristicaAsociadxsTabularInline, SolicitudCuidadosAsignacionTabularInline]
    inlines = [CaracteristicaAsociadxsTabularInline]
    readonly_fields=['ingreso', 'usuarix', 'cooperativa']
""" accion para poner 2 fechas s
    def crearInforme(self, request, queryset):
        if 'apply' in request.POST:  # if user pressed 'apply' on intermediate page
            fechaI = request.POST['fecha_inicio']
            fechaF = request.POST['fecha_fin']
            format = '%d/%m/%y'
            fi = datetime.datetime.strptime(fechaI, format)
            ff = datetime.datetime.strptime(fechaF, format)
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer)
            generarInformeAsociadx(pdf,request,queryset,fi.date(),ff.date())
            buffer.seek(0)
            messages.success(request, "Informe emitido")
            HttpResponseRedirect(request.get_full_path())
            return FileResponse(buffer, as_attachment=True, filename='Informe cliente.pdf')


        # Create form and pass the data which objects were selected before triggering 'broadcast' action
        # We create an intermediate page right here
        form = fechasForm(initial={'_selected_action': queryset.values_list('id', flat=True)})

        # We need to create a template of intermediate page with form - but this is really easy
        return render(request, './fechas.html', {'items': queryset, 'form': form})
    crearInforme.short_description = "Generar informe de asociadxs"
"""
class CooperativaAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'matricula', 'ciudad')
    search_fields = ('razon_social', 'matricula', 'ciudad')
    # inlines = [ServicioCuidadoTabularInline, AsociadxTabularInline]
    inlines = [AsociadxTabularInline]
    # data = "CARACOL - AR"
    # change_form_template = 'admin/cooperativa/cooperativa_list.html'
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class TipoServicioAdmin(admin.ModelAdmin):
    readonly_fields= ['cooperativa']

class CaracteristicaAdmin(admin.ModelAdmin):
    readonly_fields= ['cooperativa']

class CaracteristicaAsociadxsAdmin(admin.ModelAdmin):
    readonly_fields= ['cooperativa']

admin.site.register(TipoServicio, TipoServicioAdmin)
admin.site.register(ServicioCuidado, ServicioCuidadoAdmin)
admin.site.register(CaracteristicaCuidado, CaracteristicaCuidadoAdmin)
admin.site.register(ServicioCaracteristicaCuidado,ServicioCaracteristicaCuidadoAdmin)
admin.site.register(Caracteristica,CaracteristicaAdmin)
admin.site.register(CaracteristicaAsociadxs, CaracteristicaAsociadxsAdmin)
admin.site.register(Asociadx, AsociadxAdmin)
admin.site.register(Cooperativa, CooperativaAdmin)
