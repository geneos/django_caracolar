"""caracolar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from . import views
from .views import email_view

router = DefaultRouter()
router.register('users', email_view, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluimos las rutas específicas de las aplicaciones
    path('', include('home.urls')),
    path('coops/', include('coops.urls')),
    path('coops_serv/', include('coops_serv.urls')),
    path('param/', include('param.urls')),
    path('solicitudes/', include('solicitudes.urls')),
    path('clientxs/', include('clientxs.urls')),
    path('user/authentication/', include('dj_rest_auth.urls')),
    path('user/registration/', include('dj_rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    path('email_view/', include(router.urls)),
    path('email_success/', views.email_success, name='email_success')


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)

