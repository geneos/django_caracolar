from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from .models import ServicioCuidado, TipoServicio, Cooperativa
from .serializers import TipoServicioSerializer, ServicioCuidadoSerializer, CooperativaSerializer
from rest_framework import permissions

def JsonView(request):
    responseData = {
        'clave1': 'Test Response 1',
        'clave2': 'Test Response 2',
        'clave3' : 'Test Response 3'
    }

    return JsonResponse(responseData)

# Muestra todos los tipos de servicio
class tipoServicioListView(generics.ListAPIView):
    serializer_class = TipoServicioSerializer
    def get_queryset(self):
        return TipoServicio.objects.all()

# Muestra un solo tipo de servicio
class TipoServicioView(generics.ListAPIView):
    serializer_class = TipoServicioSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        id = self.kwargs['id']
        return TipoServicio.objects.filter(id=id)

# Lista de todos los servicios
class ServicioCuidadoListView(generics.ListAPIView):
    serializer_class = ServicioCuidadoSerializer

    def get_queryset(self):
        return ServicioCuidado.objects.all()

#Mostrar un servicio
class ServicioCuidadoView(generics.ListAPIView):
    serializer_class = ServicioCuidadoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        id = self.kwargs['id']
        return ServicioCuidado.objects.filter(id=id)

#mostrar todas las cooperativas pero que no se puedan agragar
class CooperativaViewList(generics.ListAPIView):
    serializer_class = CooperativaSerializer
    def get_queryset(self):
        return Cooperativa.objects.all()

# Muestra un solo una cooperativa
class CooperativaView(generics.ListAPIView):
    serializer_class = CooperativaSerializer
    def get_queryset(self):
        id = self.kwargs['id']
        return Cooperativa.objects.filter(id=id)
