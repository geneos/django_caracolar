from rest_framework import serializers

from .models import SolicitudCuidadosRecurrencia, SolicitudCuidados


class SolicitudCuidadosSerializer(serializers.ModelSerializer):
  class Meta:
    model = SolicitudCuidados
    fields = '__all__'

class SolicitudCuidadosSerializerCancelar(serializers.ModelSerializer):
  class Meta:
    model = SolicitudCuidados
    fields = ['id', 'estado']

class SolicitudCuidadosRecurrenciaSerializer(serializers.ModelSerializer):
  class Meta:
    model = SolicitudCuidadosRecurrencia
    fields = '__all__'

class SolicitudCuidadosFechasSerializer(serializers.ModelSerializer):
  class Meta:
    model = SolicitudCuidadosRecurrencia
    fields = '__all__'
