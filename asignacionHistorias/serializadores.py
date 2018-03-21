from rest_framework import serializers
from django.utils.translation import ugettext as _
from modelosGenericos import models as modelos_genericos
from .models import *
class HistoriaConAtributosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriaConAtributos
        fields = ['id_externo']

class HistoriaSimpleSerializador(serializers.ModelSerializer):
    class Meta:
        model = Historia
        fields = ['id_externo', 'puntuacionGeneral']
        
class DesarrolladorSimpleSerializador(serializers.ModelSerializer):
    class Meta:
        model = Desarrollador
        fields = ['id_externo', 'horasDisponiblesSemana']
        
class PuntuacionAtributoDesarrolladorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntuacionAtributoDesarrollador
        fields = ('id', 'desarrollador','atributo','puntuacion')
        
class PuntuacionAtributoHistoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntuacionAtributoHistoria
        fields = ('id', 'historia','atributo','puntuacion')
           
class DesarrolladorConAtributosSerializer(serializers.ModelSerializer):
    puntuaciones_atributos = PuntuacionAtributoDesarrolladorSerializer(many = True, required = True)
    class Meta:
        model = DesarrolladorConAtributos
        fields = ['id_externo', 'puntuaciones_atributos']

class ProyectoAgilSerializador(serializers.ModelSerializer):
    class Meta:
        model = modelos_genericos.ProyectoAgil
        fields = ('nombre', 'fechaInicio', 'fechaFinalizacion', "correspondenciaPuntosHoras")



class AsignacionPorHorasSerializer(serializers.ModelSerializer):
    desarrolladores =  DesarrolladorSimpleSerializador(many=True, required = True)
    historias =  HistoriaSimpleSerializador(many=True, required = True)
    class Meta:
        model = AsignacionPorHoras
        fields = ('historias', 'desarrolladores', 'relacion_horas_puntos' )
        
    def get_historias(self):
        historias = self.validated_data.get('historias')
        return [Historia(**historia) for historia in historias ]
    def get_desarrolladores(self):
        desarrolladores = self.validated_data.get('desarrolladores')
        return [Desarrollador(**desarrollador) for desarrollador in desarrolladores ]   

class AtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributo
        fields = ('id_externo', 'nombre')

     
class AsignacionPorCaracteristicasSerializer(serializers.ModelSerializer):
    desarrolladores =  DesarrolladorSimpleSerializador(many=True, required = True)
    historias =  HistoriaSimpleSerializador(many=True, required = True)
    atributos = AtributoSerializer(many=True, required = True)
    puntuaciones_atributo_historia = PuntuacionAtributoHistoriaSerializer(many = True, required = True)
    puntuaciones_atributo_desarrollador = PuntuacionAtributoDesarrolladorSerializer(many = True, required = True)
    class Meta:
        model = AsignacionPorCaracteristicas
        fields = ('historias', 'desarrolladores', 'atributos', 'procurar_misma_cantidad_tareas', 'puntuaciones_atributo_historia', 'puntuaciones_atributo_desarrollador' )
        
    def get_historias(self):
        historias = self.validated_data.get('historias')
        return [Historia(**historia) for historia in historias ]
    def get_desarrolladores(self):
        desarrolladores = self.validated_data.get('desarrolladores')
        return [Desarrollador(**desarrollador) for desarrollador in desarrolladores ]
    def get_puntuaciones_atributo_historia(self):
        puntuaciones_atributo_historia = self.validated_data.get('puntuaciones_atributo_historia')
        return [PuntuacionAtributoHistoria(**puntuacion_atributo_historia) for puntuacion_atributo_historia in puntuaciones_atributo_historia]
    def get_puntuaciones_atributo_desarrollador (self):
        puntuaciones_atributo_desarrollador = self.validated_data.get('puntuaciones_atributo_desarrollador')
        return [PuntuacionAtributoDesarrollador(**puntuacion_atributo_desarrollador) for puntuacion_atributo_desarrollador in puntuaciones_atributo_desarrollador]
    def get_procurar_misma_cantidad_tareas(self ):
        return self.validated_data.get('procurar_misma_cantidad_tareas')
    def get_atributos(self):
        atributos = self.validated_data.get('atributos')
        return [Atributo(**atributo) for atributo in atributos]
"""
class HistoriaSimpleSerializador(serializers.Serializer):
    id = serializers.IntegerField(label = _('Id historia'), required = True)
    puntuacion = serializers.IntegerField(label = _('Horas historia'),  min_value = 0, max_value = 168, required = True)

class DesarrolladorSerializer(serializers.Serializer):
    id = serializers.IntegerField(label = _('Id Desarrollador'),required = True)
    horas_disponibles_semana = serializers.IntegerField(label = _('Horas disponibles a la semana desarrollador'), min_value = 0, max_value = 168, required = True)



class AsignacionPorHorasSerializer(serializers.Serializer):
    desarrolladores = serializers.ListField(child = DesarrolladorSerializador(), required = True)
    historias = serializers.ListField(child = HistoriaSimpleSerializador(), required = True)
    relacion_horas_puntos = serializers.FloatField (required = True, min_value = 0, max_value = 2000)
"""    