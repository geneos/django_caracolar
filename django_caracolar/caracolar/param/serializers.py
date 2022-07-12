from rest_framework import serializers

from .models import Ciudad, MedioPago


class CiudadSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ciudad
    fields = '__all__'


class MedioPagoSerializer(serializers.ModelSerializer):
  class Meta:
    model = MedioPago
    fields = '__all__'
