from django.contrib import admin

# Register your models here.
from .models import Clientx, CaracteristicaClientx



class CaracteristicaClientxTabularInline(admin.TabularInline):
    model = CaracteristicaClientx
    can_delete = True

    # def has_add_permission(self, request, obj=None):
    #     return False
    #
    # def has_edit_permission(self, request, obj=None):
    #     return False

class ClientxAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'ciudad']
    search_fields = ('nombre', 'cuit', 'descripcion')
    list_filter= ('ciudad',)
    inlines = [CaracteristicaClientxTabularInline]
    readonly_fields=['ingreso', 'usuarix']

admin.site.register(Clientx, ClientxAdmin)
admin.site.register(CaracteristicaClientx)

