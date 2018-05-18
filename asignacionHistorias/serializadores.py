from rest_framework import serializers
from django.utils.translation import ugettext as _
from .models import *
class HistoriaConAtributosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriaConAtributos
        fields = ['id_externo']

class HistoriaSimpleSerializador(serializers.ModelSerializer):
    class Meta:
        model = Historia
        fields = ['id_externo', 'descripcion', 'puntuacionGeneral']
        
class DesarrolladorSimpleSerializador(serializers.Serializer):
    id_externo = serializers.IntegerField(required = True)
    nombre = serializers.CharField(required = False, max_length = 50)
    horasDisponiblesSemana = serializers.IntegerField(required = True)
        
class PuntuacionAtributoDesarrolladorSerializer(serializers.Serializer):
    atributo = serializers.IntegerField(required = True)
    puntuacion = serializers.IntegerField(required = True)
    desarrollador = serializers.IntegerField(required = True)
        
class PuntuacionAtributoHistoriaSerializer(serializers.Serializer):
    atributo = serializers.IntegerField(required = True)
    puntuacion = serializers.IntegerField(required = True)
    historia = serializers.IntegerField(required = True)

           
class DesarrolladorConAtributosSerializer(serializers.ModelSerializer):
    puntuaciones_atributos = PuntuacionAtributoDesarrolladorSerializer(many = True, required = True)
    class Meta:
        model = DesarrolladorConAtributos
        fields = ['id_externo', 'puntuaciones_atributos']
"""
class ProyectoAgilSerializador(serializers.ModelSerializer):
    class Meta:
        model = modelos_genericos.ProyectoAgil
        fields = ('nombre', 'fechaInicio', 'fechaFinalizacion', "correspondenciaPuntosHoras")
"""
class AsignacionResultantePorHorasSerializer(serializers.Serializer):
    desarrollador = DesarrolladorSimpleSerializador()
    historias = HistoriaSimpleSerializador( many = True )

class AsignacionesResultantesPorHorasSerializer(serializers.Serializer):
    asignaciones = AsignacionResultantePorHorasSerializer ( many = True )
    errores = serializers.ListField( child = serializers.CharField())

class AsignacionPorHorasSerializer(serializers.Serializer):
    desarrolladores =  DesarrolladorSimpleSerializador(many=True, required = True)
    historias =  HistoriaSimpleSerializador(many=True, required = True)
    relacion_horas_puntos = serializers.IntegerField(required = True)
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
        return [Desarrollador().fromKwargs(**desarrollador) for desarrollador in desarrolladores ]
    def get_puntuaciones_atributo_historia(self):
        puntuaciones_atributo_historia = self.validated_data.get('puntuaciones_atributo_historia')
        return puntuaciones_atributo_historia
    def get_puntuaciones_atributo_desarrollador (self):
        puntuaciones_atributo_desarrollador = self.validated_data.get('puntuaciones_atributo_desarrollador')
        return puntuaciones_atributo_desarrollador
    def get_procurar_misma_cantidad_tareas(self ):
        return self.validated_data.get('procurar_misma_cantidad_tareas')
    def get_atributos(self):
        atributos = self.validated_data.get('atributos')
        return [Atributo(**atributo) for atributo in atributos]

class GrupoHistoriasSimplesSerializador(serializers.Serializer):
    id_externo = serializers.IntegerField()
    id_historias = serializers.ListField(child=serializers.IntegerField())


class AsignacionPorCaracteristicasGurposDeHistoriasSerializer(serializers.ModelSerializer):
    desarrolladores =  DesarrolladorSimpleSerializador(many=True, required = True)
    historias =  HistoriaSimpleSerializador(many=True, required = True)
    atributos = AtributoSerializer(many=True, required = True)
    puntuaciones_atributo_historia = PuntuacionAtributoHistoriaSerializer(many = True, required = True)
    puntuaciones_atributo_desarrollador = PuntuacionAtributoDesarrolladorSerializer(many = True, required = True)
    grupos_historias = GrupoHistoriasSimplesSerializador(many=True, required = True)
    class Meta:
        model = AsignacionPorCaracteristicas
        fields = ('historias', 'grupos_historias', 'desarrolladores', 'atributos', 'procurar_misma_cantidad_tareas', 'puntuaciones_atributo_historia', 'puntuaciones_atributo_desarrollador' )
        
    def get_historias(self):
        historias = self.validated_data.get('historias')
        return [Historia(**historia) for historia in historias ]
    def get_desarrolladores(self):
        desarrolladores = self.validated_data.get('desarrolladores')
        return [Desarrollador(**desarrollador) for desarrollador in desarrolladores ]
    def get_puntuaciones_atributo_historia(self):
        puntuaciones_atributo_historia = self.validated_data.get('puntuaciones_atributo_historia')
        return puntuaciones_atributo_historia
    def get_puntuaciones_atributo_desarrollador (self):
        puntuaciones_atributo_desarrollador = self.validated_data.get('puntuaciones_atributo_desarrollador')
        return puntuaciones_atributo_desarrollador
    def get_procurar_misma_cantidad_tareas(self ):
        return self.validated_data.get('procurar_misma_cantidad_tareas')
    def get_atributos(self):
        atributos = self.validated_data.get('atributos')
        return [Atributo(**atributo) for atributo in atributos]
    def get_grupos_historias(self):
        grupo_historias = self.validated_data.get('grupos_historias')
        return grupo_historias

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