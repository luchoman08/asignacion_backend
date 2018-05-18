from django.conf.urls import url, include 
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from asignacionHistorias import views
from rest_framework_swagger.views import get_swagger_view
router = DefaultRouter()

schema_view = get_swagger_view(title='API asignación de historias')
urlpatterns = [

    url(r'^asignacionsimple/', views.AsignacionPorHorasView.as_view(),  name = 'asignacionsimple'),
    url(r'^generarAsignacionPorCaracteristicas/', views.AsignacionPorCaractericasView.as_view(),  name = 'generarAsignacionPorCaracteristicas'),
    url(r'^generarAsignacionGruposHistorias/', views.AsignacionPorCaracteristicasYGruposView.as_view(), name = 'generarAsignacionGruposHistorias'),
    


]
