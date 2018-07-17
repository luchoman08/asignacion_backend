from django.shortcuts import render
from rest_framework import viewsets, generics
from modelamientoAsignaciones import fabricaModelosLineales as fml
from .serializers import AssignmentUniqueCostSerializer, AssignmentWithAttributesSerializer
from rest_framework.renderers import CoreJSONRenderer
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
import json
# Create your views here.
class AssignmentUniqueCostView(APIView):
    permission_classes = (AllowAny, )
    @action(methods=['POST'], detail=True)
    def post(self, request, format=None):
        """
        Return task assignment based in a unique cost input
        """
        data=request.data
        serializer = AssignmentUniqueCostSerializer( data=request.data)
        if serializer.is_valid():
            resultado_dict = fml.BalancedModelFactory(serializer.get_agents(), serializer.get_tasks()).solve()
            return Response(resultado_dict)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignmentWithAttributesView(APIView):
    permission_classes = (AllowAny, )
    @action(methods=['POST'], detail=True) 
    def post(self, request, format=None):
        """
        Return task assignment based in a unique cost input
        """
        data=request.data
        serializer = AssignmentWithAttributesSerializer( data=request.data)
        if serializer.is_valid():
            #resultado_dict = fml.BalancedModelFactory(serializer.get_agents(), serializer.get_tasks()).solve()
            return Response(data)
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
            print (AsignacionResultantePorHorasSerializer(resultado_dict[0]).data)
            return Response(AsignacionesResultantesPorHorasSerializer(resultado_dict))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AsignacionPorCaracteristicasYGruposView(generics.GenericAPIView):
    def get_serializer_class(self):
        return AsignacionPorCaracteristicasGurposDeHistoriasSerializer
    def get_queryset(self):
        return AsignacionPorCaracteristicasYGrupos.objects.all()
    def patch(self, request, format=None):
        """
        Retornar una asignación simple basado en los datos de entrada
        """
        data=request.data
        serializer = AsignacionPorCaracteristicasGurposDeHistoriasSerializer( data=request.data)
       
        if serializer.is_valid():
            #serializer.save()
            print(serializer.get_grupos_historias())
            asignacion = AsignacionPorCaracteristicasGurposDeHistoriasSerializer(serializer.validated_data)
            resultado_dict = fml.FabricaModeloPorAtributosConGruposHistorias(serializer.get_desarrolladores(), serializer.get_historias(), \
            serializer.get_grupos_historias(), serializer.get_atributos(), \
            serializer.get_puntuaciones_atributo_desarrollador(), serializer.get_puntuaciones_atributo_historia(), \
            serializer.get_procurar_misma_cantidad_tareas()).solve()
            return Response(resultado_dict)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
