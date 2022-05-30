from django.urls import path
from . import views

urlpatterns = [
    path('jsoncoops', views.JsonView, name='jsoncoops')
]
