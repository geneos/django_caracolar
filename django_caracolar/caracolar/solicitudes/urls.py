from django.urls import path
from . import views

urlpatterns = [
    path('', views.SolicitudesView, name='solicitudes'),
]
