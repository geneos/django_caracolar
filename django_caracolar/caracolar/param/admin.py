from django.contrib import admin
from .models import Pais, Provincia, Ciudad, MedioPago

# Register your models here.
admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Ciudad)
admin.site.register(MedioPago)
