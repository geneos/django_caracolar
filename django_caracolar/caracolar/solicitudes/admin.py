from django.contrib import admin, messages

# Register your models here.
from django.contrib.admin.helpers import ActionForm
from django import forms
from django.http import HttpResponse
#from lxml.html.builder import HTML

from .models import SolicitudCuidadosRecurrencia, SolicitudCuidadosFechas, SolicitudCuidados


class SolicitudCuidadosRecurrenteTabularInline(admin.TabularInline):
    model = SolicitudCuidadosRecurrencia
    can_delete = True

class SolicitudCuidadosFechasTabularInline(admin.TabularInline):
    model = SolicitudCuidadosFechas
    can_delete = True

class UpdateActionForm(ActionForm):
	monto = forms.IntegerField()

class SolicitudCuidadosAdmin(admin.ModelAdmin):
    icon_name = 'gamepad'
    action_form = UpdateActionForm
    inlines = [SolicitudCuidadosRecurrenteTabularInline, SolicitudCuidadosFechasTabularInline]

    list_display = ['fecha', 'clientx', 'servicio', 'estado']

    @admin.action(description='Asignar estado')
    def asignar(self, request, queryset):
        print("ENTRA")
        # queryset.update(estado=2)
        messages.success(request, "Estado Actualizado correctamente")

    @admin.action(description="Registrar Pago")
    def registrarPago(self, request, queryset):
        monto_str = request.POST['monto']
        print("Monto " + monto_str)
        monto = float(monto_str)
        queryset.update(montoPagado=monto)
        messages.success(request, "Monto Pagado Actualizado correctamente")

    # @admin.action(description="Informe 2")
    # def emitirInforme2(self, request, queryset):
        # Create file to recieve data and create the PDF
        # buffer = BytesIO()
        #
        # # Create the file PDF
        # pdf = canvas.Canvas(buffer)
        #
        # # Inserting in PDF where this 2 first arguments are axis X and Y respectvely
        # pdf.drawString(50, 800, "Some Title")
        #
        # w, h = A4
        # xlist = [10, 60, 110, 160]
        # ylist = [h - 10, h - 60, h - 110, h - 160]
        # pdf.grid(xlist, ylist)
        #
        # pdf.showPage()
        # pdf.save()
        #
        # # Retrieving the file to start
        # buffer.seek(0)
        #
        # messages.success(request, "Informe emitido")
        #
        # # as_attachment=True to make file as an attachment to download
        # return FileResponse(buffer, as_attachment=True, filename='report.pdf')


    #@admin.action(description="Informe")
    #def emitirInforme(self, request, queryset):
    #    htmlstring="<HTML><HEAD><TITLE>Un t&iacute;tulo principal</TITLE></HEAD><BODY><H1>Otro t&iacute;tulo principal</H1></BODY></HTML>"
    #    html = HTML(string=htmlstring)
    #    main_doc = html.render()
    #    pdf = main_doc.write_pdf()
    #    return HttpResponse(pdf, content_type='application/pdf')

    admin.site.add_action(asignar, "Asignar Estado")
    admin.site.add_action(registrarPago, "Registrar Pago")
    #admin.site.add_action(emitirInforme, "Informe 1")
    # admin.site.add_action(emitirInforme2, "Informe 2")

    # actions = [asignar, registrarPago]
    # actions = ['asignar', 'registrarPago']

admin.site.register(SolicitudCuidados,SolicitudCuidadosAdmin)
