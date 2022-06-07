from django.contrib import admin
from .models import Cooperativa, TipoServicio, ServicioCuidado, CaracteristicaCuidado, ServicioCaracteristicaCuidado, \
    Asociadx, CaracteristicaAsociadxs, Caracteristica

# Register your models here.
admin.site.register(TipoServicio)
admin.site.register(CaracteristicaCuidado)
admin.site.register(ServicioCaracteristicaCuidado)

class ServicioCaracteristicaCuidadoInline(admin.TabularInline):
    model = ServicioCaracteristicaCuidado
    can_delete = True

class ServicioCuidadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'costoReferencia')
    search_fields = ('nombre', 'descripcion')
    inlines = [ServicioCaracteristicaCuidadoInline]

admin.site.register(ServicioCuidado, ServicioCuidadoAdmin)

class AsociadxTabularInline(admin.TabularInline):
    model = Asociadx
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False

class CaracteristicaAsociadxsTabularInline(admin.TabularInline):
    model = CaracteristicaAsociadxs
    can_delete = True

    # def has_add_permission(self, request, obj=None):
    #     return False
    #
    # def has_edit_permission(self, request, obj=None):
    #     return False

class AsociadxAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'ciudad', 'ingreso')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter= ('ciudad',)
    # inlines = [CaracteristicaAsociadxsTabularInline, SolicitudCuidadosAsignacionTabularInline]
    inlines = [CaracteristicaAsociadxsTabularInline]
    readonly_fields=['ingreso', 'usuarix']

admin.site.register(Asociadx, AsociadxAdmin)

class CooperativaAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'matricula', 'ciudad')
    search_fields = ('razon_social', 'matricula', 'ciudad')
    # inlines = [ServicioCuidadoTabularInline, AsociadxTabularInline]
    inlines = [AsociadxTabularInline]
    # data = "CARACOL - AR"
    # change_form_template = 'admin/cooperativa/cooperativa_list.html'

admin.site.register(Caracteristica)
admin.site.register(CaracteristicaAsociadxs)

admin.site.register(Cooperativa, CooperativaAdmin)
