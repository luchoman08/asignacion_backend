from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^obtenerAsignacion/', views.asignacionHistorias,  name = 'obtenerAsignacion')
]
