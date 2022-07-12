from django.urls import path, include, re_path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# En el router vamos añadiendo los endpoints a los viewsets

urlpatterns = [
    path('jsoncoops', views.JsonView, name='jsoncoops'),
   # path('', include(router.urls)),
    re_path('^servicio/(?P<id>.+)/$', views.ServicioCuidadoView.as_view()),
    re_path('^tiposervicios/', views.tipoServicioListView.as_view()),
    re_path('^servicioscuidados/', views.ServicioCuidadoListView.as_view()),
    re_path('^tiposervicio/(?P<id>.+)/$', views.TipoServicioView.as_view()),
    re_path('^cooperativa/(?P<id>.+)/$', views.CooperativaView.as_view()),
    re_path('^cooperativalist/', views.CooperativaViewList.as_view())#todas las cooperativas pero no se puedan agragar

]
