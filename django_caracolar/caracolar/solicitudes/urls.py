from django.urls import path, include, re_path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# En el router vamos añadiendo los endpoints a los viewsets
#router.register('recurrente', views.SolicitudCuidadosRecurrenciaList)
router.register('fechas', views.SolicitudCuidadosFechasList)
router.register('recurrente', views.SolicitudCuidadosRecurrenciaListview)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^solicitudcuidados/(?P<id>.+)/$', views.SolicitudCuidadosView.as_view()),
    re_path(r'^solicitudcuidados/$', views.SolicitudCuidadosView.as_view()),
    #path('recurrente/', views.SolicitudCuidadosRecurrenciaList.as_view()),
]
