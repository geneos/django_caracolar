from rest_framework import serializers

from .models import TipoServicio, ServicioCuidado, Cooperativa


class TipoServicioSerializer(serializers.ModelSerializer):
  class Meta:
    model = TipoServicio
    fields = '__all__'


class ServicioCuidadoSerializer(serializers.ModelSerializer):
  class Meta:
    model = ServicioCuidado
    fields = '__all__'

class CooperativaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cooperativa
    fields = '__all__'
