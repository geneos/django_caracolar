from django.urls import path
from . import views

urlpatterns = [
    path('', views.ParamView, name='parametros'),
]
