from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .models import SolicitudCuidadosRecurrencia, SolicitudCuidadosFechas, SolicitudCuidados
from .serializers import SolicitudCuidadosRecurrenciaSerializer, SolicitudCuidadosFechasSerializer, \
    SolicitudCuidadosSerializer, SolicitudCuidadosSerializerCancelar


# lista y add de Solicitud Cuidados
class SolicitudCuidadosView(generics.ListAPIView):
    serializer_class = SolicitudCuidadosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return SolicitudCuidados.objects.get(id=id)
        except SolicitudCuidados.DoesNotExist:
            return None

    def get_queryset(self):
        if 'id' not in self.kwargs:
            return SolicitudCuidados.objects.all()
        return SolicitudCuidados.objects.filter(id=self.kwargs['id'])

    def patch(self, request, *args, **kwargs):
        todo_id = self.kwargs['id']
        todo_instance = self.get_object(todo_id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'id':todo_id,
            'estado': 4,
        }
        serializer = SolicitudCuidadosSerializerCancelar(instance=todo_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lista y add de solicitud cuidado por fecha
class SolicitudCuidadosFechasList(viewsets.ModelViewSet):
    queryset = SolicitudCuidadosFechas.objects.all()
    serializer_class = SolicitudCuidadosFechasSerializer
    permission_classes = [permissions.IsAuthenticated]

# Lista y add de solicitud cuidado recurrente
class SolicitudCuidadosRecurrenciaListview(viewsets.ModelViewSet):
    queryset = SolicitudCuidadosRecurrencia.objects.all()
    serializer_class = SolicitudCuidadosRecurrenciaSerializer
    permission_classes = [permissions.IsAuthenticated]

