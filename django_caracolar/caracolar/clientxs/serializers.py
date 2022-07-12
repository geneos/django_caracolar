
from .models import Clientx, CaracteristicaClientx
from rest_framework import serializers

class ClientxSerializer(serializers.ModelSerializer):
  class Meta:
    model = Clientx
    # fields = ['id', 'titulo', 'imagen', 'estreno', 'resumen']
    fields = '__all__'

class CaracteristicaClientxSerializer(serializers.ModelSerializer):
  class Meta:
    model = CaracteristicaClientx
    fields = '__all__'
