from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^obtenerAsignacion/', views.asignacionHistorias,  name = 'obtenerAsignacion'),
    url(r'^historias/(?P<pk>[0-9]+)/$', views.HistoriaDetalle.as_view(), name = 'historiaDetalle'),
    url(r'^historias/', views.HistoriaListado.as_view(), name = 'historiaListado'),
    url(r'^proyectoAgil/(?P<pk>[0-9]+)/$', views.ProyectoAgilDetalle.as_view(), name = 'proyectoAgilDetalle'),
    url(r'^proyectoAgil/', views.ProyectoAgilListado.as_view(), name = 'proyectoAgilListado'),
    url(r'^desarrollador/(?P<pk>[0-9]+)/$', views.DesarrolladorDetalle.as_view(), name = 'desarrolladorAgilDetalle'),
    url(r'^desarrollador/', views.DesarrolladorListado.as_view(), name = 'desarroladorAgilListado'),
    
]
