from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, generics, status

from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
# Create your views here.
from .models import Clientx, CaracteristicaClientx
from .serializers import ClientxSerializer, CaracteristicaClientxSerializer
from rest_framework import permissions

#Muestra todos los clientes
class ClientxsListView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Clientx.objects.all()
    serializer_class = ClientxSerializer

#Muestra solo un cliente por ID y se puede eliminar
class ClientxView(generics.ListAPIView):
    serializer_class = ClientxSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, cliente_id):
        try:
            return Clientx.objects.get(id=cliente_id)
        except Clientx.DoesNotExist:
            return None

    def get_queryset(self):
        id = self.kwargs['id']
        return Clientx.objects.filter(id=id)

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        todo_instance = self.get_object(id)
        if not todo_instance:
            return Response(
                {"res": "No exixte cliente con ese ID"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Cliente borrado!"},
            status=status.HTTP_200_OK
        )


class CaracteristicaClientxView(generics.ListAPIView):
    serializer_class = CaracteristicaClientxSerializer
    permission_classes = [permissions.IsAuthenticated]

    #Mostrar caracteristicas del clientx
    def get_queryset(self):
        id = self.kwargs['id']
        return CaracteristicaClientx.objects.filter(clientx=id)

    #crear caracteristica
    def post(self, request, *args, **kwargs):
            data = {
                'clientx': self.kwargs['id'],
                'caracteristica': request.data.get('caracteristica'),
                'cooperativa': request.data.get('cooperativa'),

            }
            serializer = CaracteristicaClientxSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CaracteristicaClientxViewDelete(generics.ListAPIView):
    serializer_class = CaracteristicaClientxSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        id_c=self.kwargs['id_c']
        id=self.kwargs['id']
        return CaracteristicaClientx.objects.filter(clientx=id_c, id=id)

    def get_object(self, caracteristica_id, id_cliente):
        try:
            return CaracteristicaClientx.objects.get(id=caracteristica_id, clientx=id_cliente)
        except CaracteristicaClientx.DoesNotExist:
            return None

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        id_cliente=self.kwargs['id_c']
        todo_instance = self.get_object(id, id_cliente)
        if not todo_instance:
            return Response(
                {"res": "No exixte caracteristica con ese ID"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Caracteristica borrada!"},
            status=status.HTTP_200_OK
        )
