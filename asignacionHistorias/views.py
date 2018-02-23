from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics
from .models import *
from modelamientoAsignaciones import fabricaModelosLineales as fml
from modelamientoAsignaciones import asignacion
from .serializadores import *

from modelosGenericos import models as modelos_genericos

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class HistoriaDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = modelos_genericos.Historia.objects.all()
    serializer_class = HistoriaSerializador
    
class HistoriaListado(generics.ListCreateAPIView):
    queryset = modelos_genericos.Historia.objects.all()
    serializer_class = HistoriaSerializador

class ProyectoAgilDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = modelos_genericos.ProyectoAgil.objects.all()
    serializer_class = ProyectoAgilSerializador
    
class ProyectoAgilListado(generics.ListCreateAPIView):
    queryset = modelos_genericos.ProyectoAgil.objects.all()
    serializer_class = ProyectoAgilSerializador

class DesarrolladorDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = modelos_genericos.Desarrollador.objects.all()
    serializer_class = DesarrolladorSerializador
    
class DesarrolladorListado(generics.ListCreateAPIView):
    queryset = modelos_genericos.Desarrollador.objects.all()
    serializer_class = DesarrolladorSerializador
        
def asignacionHistorias(request):
    historias = modelos_genericos.Historia.objects.all()
    desarrolladores = modelos_genericos.Desarrollador.objects.all()
    asignacionObj = asignacion.ModeloAsignaciones(desarrolladores, historias,  asignacion.TipoAsignacion.sencilla)
    modelo_lineal_simple = fml.FabricaModeloEquilibrado(asignacionObj)
    print(modelo_lineal_simple.initNombreDesarrolladores())

    return HttpResponse(
        "Hasta si, cantidad desarrolladores = " + str(asignacionObj.cantidadDesarrolladores)+
        "Hasta si, cantidad historias = " + str(asignacionObj.cantidadHistorias))