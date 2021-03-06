import os
from datetime import date, timedelta
from io import BytesIO

from django.contrib import admin, messages

# Register your models here.
from django.http import FileResponse
from reportlab.pdfgen import canvas

from .models import Clientx, CaracteristicaClientx
from solicitudes.models import SolicitudCuidados, SolicitudCuidadosRecurrencia,SolicitudCuidadosFechas

class CaracteristicaClientxTabularInline(admin.TabularInline):
    model = CaracteristicaClientx
    can_delete = True
    readonly_fields = ['cooperativa']

    # def has_add_permission(self, request, obj=None):
    #     return False
    #
    # def has_edit_permission(self, request, obj=None):
    #     return False
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

def infoCliente(pdf,x,y,d):
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

#Informe del cliente solo para las solicitudes activas(pendientes o asignadas
def generarInformeCliente(pdf,request,queryset):
    settings_dir = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    img = os.path.join(PROJECT_ROOT, 'admin-interface/logo/logo.png')
    pdf.drawImage(img, 22,720,550,100)
    set = queryset.all()
    y = 700
    x = 45
    e = 15
    pdf.setFont("Helvetica", 12)
    pdf.drawString(x, y, 'INFORME DEL CLIENTE')
    pdf.setFont("Helvetica", 10)
    y= y-15
    if set.count()>1:
        return messages.error(request,'Debe seleccionar solo un cliente')
    else:
        for d in set:
            y=infoCliente(pdf,x,y,d)
            solicitudes = SolicitudCuidados.objects.filter(clientx = d.id)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(x, y, 'SERVICIOS')
            for s in solicitudes:
                y = y-15
                if s.estado == 1 or s.estado == 2:
                    pdf.setFont("Helvetica-Bold", 10)
                    pdf.drawString(x, y, 'Nombre: '+str(s.servicio.nombre))
                    y=y-15
                    pdf.drawString(x, y, 'Costo referencial: '+str(s.servicio.costoReferencia))
                    y=y-15
                    pdf.drawString(x, y, 'Cooperativa: '+str(s.servicio.cooperativa))
                    y=y-15
                    if s.estado == 1:
                        pdf.drawString(x, y, 'Estado: Pendiente')
                    else:
                        pdf.drawString(x, y, 'Estado: Asignada')
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

@admin.action(description="Informe del cliente de solicitudes activas")
def emitirInformeCliente(self, request, queryset):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        generarInformeCliente(pdf,request,queryset)
        buffer.seek(0)
        messages.success(request, "Informe emitido")
        return FileResponse(buffer, as_attachment=True, filename='Informe cliente.pdf')

#Informe del cliente con el historial de solicutudes de un mes
def generarInformeClienteHistorial(pdf,request,queryset):
    settings_dir = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    img = os.path.join(PROJECT_ROOT, 'admin-interface/logo/photo4976484941684648281.png')
    pdf.drawImage(img, 22,720,550,100)
    set = queryset.all()
    y = 700
    x = 45
    e = 15
    pdf.setFont("Helvetica", 12)
    pdf.drawString(x, y, 'INFORME DEL CLIENTE')
    pdf.setFont("Helvetica", 10)
    y= y-15
    if set.count()>1:
        return messages.error(request,'Debe seleccionar solo un cliente')
    else:
        for d in set:
            y= infoCliente(pdf, x, y,d)
            today = date.today()
            td = timedelta(30)
            mesAtras= today - td
            solicitudes = SolicitudCuidados.objects.filter(clientx = d.id)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(x, y, 'SERVICIOS')
            for s in solicitudes:
                if s.fecha < today and s.fecha > mesAtras:
                    y = y-15
                    pdf.setFont("Helvetica-Bold", 10)
                    pdf.drawString(x, y, 'Nombre: '+str(s.servicio.nombre))
                    y=y-15
                    pdf.drawString(x, y, 'Costo referencial: '+str(s.servicio.costoReferencia))
                    y=y-15
                    pdf.drawString(x, y, 'Cooperativa: '+str(s.servicio.cooperativa))
                    y=y-15
                    if s.estado == 1:
                        pdf.drawString(x, y, 'Estado: Pendiente')
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

@admin.action(description="Informe del hostorial del cliente")
def emitirInformeClienteHistorial(self, request, queryset):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        generarInformeClienteHistorial(pdf,request,queryset)
        buffer.seek(0)
        messages.success(request, "Informe emitido")
        return FileResponse(buffer, as_attachment=True, filename='Informe cliente.pdf')


class ClientxAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'ciudad']
    search_fields = ('nombre', 'cuit', 'descripcion')
    list_filter= ('ciudad',)
    inlines = [CaracteristicaClientxTabularInline]
    readonly_fields=['ingreso', 'usuarix', 'cooperativa']
    actions = [emitirInformeCliente, emitirInformeClienteHistorial]

class CaracteristicaClientxAdmin(admin.ModelAdmin):
    readonly_fields = ['cooperativa']

admin.site.register(Clientx, ClientxAdmin)
admin.site.register(CaracteristicaClientx,CaracteristicaClientxAdmin)

