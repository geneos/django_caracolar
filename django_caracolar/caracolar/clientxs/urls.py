from django.urls import path, include, re_path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
# En el router vamos añadiendo los endpoints a los viewsets
router.register('listclientxs', views.ClientxsListView) #todos los clientes

urlpatterns = [
    path('', include(router.urls)),
    re_path('^clientx/(?P<id>.+)$', views.ClientxView.as_view()),
    re_path('^caracteristicas/(?P<id>.+)$', views.CaracteristicaClientxView.as_view()),
    re_path(r'^caracteristicas/(?P<id_c>\d+)/(?P<id>\d+)/$', views.CaracteristicaClientxViewDelete.as_view()),
]

