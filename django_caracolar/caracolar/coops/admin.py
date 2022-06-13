from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .form import fechasForm
from .models import Cooperativa, TipoServicio, ServicioCuidado, CaracteristicaCuidado, ServicioCaracteristicaCuidado, \
    Asociadx, CaracteristicaAsociadxs, Caracteristica

# Register your models here.


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

class AsociadxAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'ciudad', 'ingreso')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter= ('ciudad',)
    actions = ['crearInforme']
    # inlines = [CaracteristicaAsociadxsTabularInline, SolicitudCuidadosAsignacionTabularInline]
    inlines = [CaracteristicaAsociadxsTabularInline]
    readonly_fields=['ingreso', 'usuarix', 'cooperativa']

    def crearInforme(self, request, queryset):
        if 'apply' in request.POST:  # if user pressed 'apply' on intermediate page
            print(request.POST['fecha_inicio'])
            print(request.POST['fecha_fin'])
            # LLAMAR A LA FUNCION PARA CREAR EL INFORME
            # Return to previous page
            return HttpResponseRedirect(request.get_full_path())

        # Create form and pass the data which objects were selected before triggering 'broadcast' action
        # We create an intermediate page right here
        form = fechasForm(initial={'_selected_action': queryset.values_list('id', flat=True)})

        # We need to create a template of intermediate page with form - but this is really easy
        return render(request, './fechas.html', {'items': queryset, 'form': form})
    crearInforme.short_description = "Generar informe de asociadxs"

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
