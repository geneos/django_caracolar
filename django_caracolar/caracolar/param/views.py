from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from .models import Ciudad, MedioPago
from .serializers import CiudadSerializer, MedioPagoSerializer
from rest_framework import permissions

#mostrar todas las ciudades pero no se puedan agragar
class CiudadViewList(generics.ListAPIView):
    serializer_class = CiudadSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Ciudad.objects.all()

#mostrar todas los medios de pago pero no se puedan agragar
class MedioPagoViewList(generics.ListAPIView):
    serializer_class = MedioPagoSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return MedioPago.objects.all()

