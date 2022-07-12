from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path('^ciudades/', views.CiudadViewList.as_view()),
    re_path('^mediospago/', views.MedioPagoViewList.as_view())
]
