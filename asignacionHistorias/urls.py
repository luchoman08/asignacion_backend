from django.conf.urls import url, include 
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from asignacionHistorias import views
from rest_framework_swagger.views import get_swagger_view
router = DefaultRouter()
router.register(r'generarAsignacionSimple', views.AsignacionPorHorasView.as_view(), base_name='generarAsignacionSimple')

schema_view = get_swagger_view(title='API asignación de historias')
urlpatterns = [
    url(r'^$', schema_view, name = "swagger_api_view"),
    url(r'^', include(router.urls)),
    url(r'^generarAsignacionSimple/', views.AsignacionPorHorasView.as_view(),  name = 'generarAsignacionSimple'),
    url(r'^proyectoAgil/', views.ProyectoAgilListado.as_view(), name = 'proyectoAgilListado'),
    url(r'^historiasConAtributos/(?P<pk>[0-9]+)/$', views.HistoriaConAtributosDetalle.as_view(), name = 'historiaDetalle'),
    url(r'^historiasConAtributos/', views.HistoriaConAtributosList.as_view(), name = 'historiaConAtributosListado'),
    url(r'^desarrolladoresConAtributos/(?P<pk>[0-9]+)/$', views.DesarrolladorConAtributosDetalle.as_view(), name = 'desarrolladorDetalle'),
    url(r'^desarrolladoresConAtributos/', views.DesarrolladorConAtributosList.as_view(), name = 'desarrolladorListado'),
    url(r'^atributos/(?P<pk>[0-9]+)/$', views.AtributoDetalle.as_view(), name = 'atributoDetalle'),
    url(r'^atributos/', views.AtributoList.as_view(), name = 'atributoListado'),
    url(r'^puntuacionAtributoDesarrollador/(?P<pk>[0-9]+)/$', views.PuntuacionAtributoDesarrolladorDetalle.as_view(), name = 'puntuacionDesarrolladorAtributoDetalle'),
    url(r'^puntuacionAtributoDesarrollador/', views.PuntuacionAtributoDesarrolladorList.as_view(), name = 'puntuacionDesarrolladorAtributoListado'),
    url(r'^puntuacionAtributoHistoria/(?P<pk>[0-9]+)/$', views.PuntuacionAtributoHistoriaDetalle.as_view(), name = 'puntuacionHistoriaAtributoDetalle'),
    url(r'^puntuacionAtributoHistoria/$', views.PuntuacionAtributoHistoriaList.as_view(), name = 'puntuacionHistoriaAtributoListado'),
    

]
"""
    #url(r'^obtenerAsignacion/', views.asignacionHistorias,  name = 'obtenerAsignacion'),
    url(r'^historias/(?P<pk>[0-9]+)/$', views.HistoriaDetalle.as_view(), name = 'historiaDetalle'),
    url(r'^historias/', views.HistoriaListado.as_view(), name = 'historiaListado'),
    url(r'^historiasSimples/', views.HistoriaSimpleCrear.as_view(), name = 'historiaSimpleCrear'),
    url(r'^proyectoAgil/(?P<pk>[0-9]+)/$', views.ProyectoAgilDetalle.as_view(), name = 'proyectoAgilDetalle'),
    url(r'^proyectoAgil/', views.ProyectoAgilListado.as_view(), name = 'proyectoAgilListado'),
    url(r'^desarrollador/(?P<pk>[0-9]+)/$', views.DesarrolladorDetalle.as_view(), name = 'desarrolladorAgilDetalle'),
    url(r'^desarrollador/', views.DesarrolladorListado.as_view(), name = 'desarroladorAgilListado'),
"""