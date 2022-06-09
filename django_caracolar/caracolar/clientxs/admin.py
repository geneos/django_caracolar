import os
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

#Funcion donde se genea la tabla con la información de las solicitudes de cuidado recurrentes para el informe
def tablaSolicitudesRecurrentes(s, pdf,x,y):
    pdf.drawString(x, y+1, 'Servicios recurrentes')
    solicitudRecurrente= SolicitudCuidadosRecurrencia.objects.filter(solicitud= s.id)
    y=y-2
    cabeceraTablaServiciosRecurrente(pdf,y)
    y=y-18
    for sr in solicitudRecurrente:
        xlist = [45, 132, 217, 329, 468]
        ylist = [y, y-18]
        pdf.grid(xlist, ylist)
        if str(sr.dia) == 1:
            pdf.drawString(48, y-16, "Lunes")
        if str(sr.dia) == 2:
            pdf.drawString(48, y-16, "Martes")
        if str(sr.dia) == 3:
            pdf.drawString(48, y-16, "Miércoles")
        if str(sr.dia) == 4:
            pdf.drawString(48, y-16, "Jueves")
        if str(sr.dia) == 5:
            pdf.drawString(48, y-16, "Viernes")
        if str(sr.dia) == 6:
            pdf.drawString(48, y-16, "Sábado")
        if str(sr.dia) == 7:
            pdf.drawString(48, y-16, "Domingo")
        pdf.drawString(135, y-16,str(sr.horaInicio))
        pdf.drawString(220, y-16,str(sr.horaFin))
        pdf.drawString(332, y-16,str(sr.tiempo))
        y = y-18
        if (y<50):
            y = 800
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            cabeceraTablaServiciosRecurrente(pdf,y)
            pdf.setFont("Helvetica", 10)
            y = y-18

def tablaSolicitudesFecha(s, pdf,x,y):
    pdf.drawString(x, y+1, 'Servicios por fecha')
    solicitudFecha= SolicitudCuidadosFechas.objects.filter(solicitud= s.id)
    y=y-2
    cabeceraTablaServiciosFecha(pdf,y)
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
            pdf.setFont("Helvetica", 10)
            cabeceraTablaServiciosFecha(pdf,y)
            pdf.setFont("Helvetica", 10)
            y = y-18

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
            solicitudes = SolicitudCuidados.objects.filter(clientx = d.id)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(x, y, 'SERVICIOS')
            y = y-15
            for s in solicitudes:
                pdf.drawString(x, y, 'Nombre: '+str(s.servicio.nombre))
                y=y-15
                pdf.drawString(x, y, 'Costo referencial: '+str(s.servicio.costoReferencia))
                y=y-15
                pdf.drawString(x, y, 'Cooperativa: '+str(s.servicio.cooperativa))
                y=y-18
                if s.recurrencia:
                    tablaSolicitudesRecurrentes(s, pdf,x,y)
                else:
                    tablaSolicitudesFecha(s,pdf,x,y)


        pdf.showPage()
        pdf.save()

@admin.action(description="Informe del cliente")
def emitirInformeCliente(self, request, queryset):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        generarInformeCliente(pdf,request,queryset)
        buffer.seek(0)
        messages.success(request, "Informe emitido")
        return FileResponse(buffer, as_attachment=True, filename='Informe cliente.pdf')


class ClientxAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'ciudad']
    search_fields = ('nombre', 'cuit', 'descripcion')
    list_filter= ('ciudad',)
    inlines = [CaracteristicaClientxTabularInline]
    readonly_fields=['ingreso', 'usuarix']
    actions = [emitirInformeCliente]

admin.site.register(Clientx, ClientxAdmin)
admin.site.register(CaracteristicaClientx)

