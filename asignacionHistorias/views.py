from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics
from .models import *
from modelamientoAsignaciones import fabricaModelosLineales as fml
from modelamientoAsignaciones import asignacion
from .serializadores import *
from modelosGenericos import models as modelos_genericos
from rest_framework.renderers import CoreJSONRenderer
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class AsignacionPorHorasView(generics.GenericAPIView):
    def get_serializer_class(self):
        return AsignacionPorHorasSerializer
    def get_queryset(self):
        return AsignacionPorHoras.objects.all()
    def patch(self, request, format=None):
        """
        Retornar una asignación simple basado en los datos de entrada
        """
        data=request.data
        serializer = AsignacionPorHorasSerializer( data=request.data)
       
        if serializer.is_valid():
            #serializer.save()
            asignacion = AsignacionPorHoras(serializer.validated_data)
            resultado_dict = fml.FabricaModeloEquilibrado(serializer.get_desarrolladores(), serializer.get_historias(), 1).solve()
            return Response(resultado_dict)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AsignacionPorCaractericasView(generics.GenericAPIView):
    def get_serializer_class(self):
        return AsignacionPorCaracteristicasSerializer
    def get_queryset(self):
        return AsignacionPorCaracteristicas.objects.all()
    def patch(self, request, format=None):
        """
        Retornar una asignación simple basado en los datos de entrada
        """
        data=request.data
        serializer = AsignacionPorCaracteristicasSerializer( data=request.data)
       
        if serializer.is_valid():
            #serializer.save()
            asignacion = AsignacionPorCaracteristicas(serializer.validated_data)
            resultado_dict = fml.FabricaModeloPorAtributos(serializer.get_desarrolladores(), serializer.get_historias(), \
            serializer.get_atributos(), \
            serializer.get_puntuaciones_atributo_desarrollador(), serializer.get_puntuaciones_atributo_historia(), \
            serializer.get_procurar_misma_cantidad_tareas()).solve()
            return Response(resultado_dict)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HistoriaSimpleCrear(generics.CreateAPIView):
    serializer_class = AsignacionPorHorasSerializer
class ProyectoAgilListado(generics.ListCreateAPIView):
    queryset = modelos_genericos.ProyectoAgil.objects.all()
    serializer_class = ProyectoAgilSerializador    
    
    
class HistoriaConAtributosList(generics.ListCreateAPIView):

    queryset = HistoriaConAtributos.objects.all()
    serializer_class = HistoriaConAtributosSerializer

class HistoriaConAtributosDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistoriaConAtributos.objects.all()
    serializer_class = HistoriaConAtributosSerializer
    
class AtributoList(generics.ListCreateAPIView):
    queryset = Atributo.objects.all()
    serializer_class = AtributoSerializer

class AtributoDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Atributo.objects.all()
    serializer_class = AtributoSerializer 

class PuntuacionAtributoDesarrolladorList(generics.ListCreateAPIView):
    queryset = PuntuacionAtributoDesarrollador.objects.all()
    serializer_class = PuntuacionAtributoDesarrolladorSerializer
    
class PuntuacionAtributoDesarrolladorDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = PuntuacionAtributoDesarrollador.objects.all()
    serializer_class = PuntuacionAtributoDesarrolladorSerializer
    
class PuntuacionAtributoHistoriaList(generics.ListCreateAPIView):
    queryset = PuntuacionAtributoHistoria.objects.all()
    serializer_class = PuntuacionAtributoHistoriaSerializer
    
class PuntuacionAtributoHistoriaDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = PuntuacionAtributoHistoria.objects.all()
    serializer_class = PuntuacionAtributoHistoriaSerializer
  
class DesarrolladorConAtributosDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = DesarrolladorConAtributos.objects.all()
    serializer_class = DesarrolladorConAtributosSerializer
    
class DesarrolladorConAtributosList(generics.ListCreateAPIView):
    queryset = DesarrolladorConAtributos.objects.all()
    serializer_class = DesarrolladorConAtributosSerializer
        
""" 
class HistoriaViewSets(viewsets.ReadOnlyModelViewSet):

    queryset = modelos_genericos.Historia.objects.all()
    serializer_class = HistoriaSerializador

class HistoriaDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = modelos_genericos.Historia.objects.all()
    serializer_class = HistoriaSerializador

class HistoriaSimpleCrear(generics.CreateAPIView):
    serializer_class = AsignacionPorHorasSerializer

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
"""
