from django.conf.urls import url, include 
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from asignacionHistorias import views

urlpatterns = [

    url(r'^uniquecostassign/', views.AssignmentUniqueCostView.as_view(),  name = 'uniquecostassign')


]
