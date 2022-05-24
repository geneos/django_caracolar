from django.urls import path
from . import views

urlpatterns = [
    path('', views.CoopsServView, name='cooperativas'),
]
