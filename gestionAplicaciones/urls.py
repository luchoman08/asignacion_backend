from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^adicionarAplicacion/', views.adicionarAplicacion, name = 'adicionarApp'),
    url(r'^datosAplicacion/', views.DatosAplicacion.as_view(), name = 'verAplicacion'),
    url(r'^vistaAPI/', views.vistaAPI, name = 'vistaAPI'),
    ]
    
