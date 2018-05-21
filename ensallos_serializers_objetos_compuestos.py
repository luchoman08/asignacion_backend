from rest_framework import serializers


class Historia(object):
    """
    Almacena una historia de usuario
    """
    def __init__( self, id_externo=None, puntuacionGeneral = None ):
        self.id_externo = id_externo
        self.puntuacionGeneral = puntuacionGeneral


class HistoriaSimpleSerializador(serializers.Serializer):
    id_externo = serializers.IntegerField(required = True)
    puntuacionGeneral = serializers.IntegerField(required = True)
        
class DesarrolladorSimpleSerializador(serializers.Serializer):
    id_externo = serializers.IntegerField(required = True)
    horasDisponiblesSemana = serializers.IntegerField(required = True)
        
class PuntuacionAtributoDesarrolladorSerializer(serializers.Serializer):
    atributo = serializers.IntegerField(required = True)
    puntuacion = serializers.IntegerField(required = True)
    desarrollador = serializers.IntegerField(required = True)
        
class PuntuacionAtributoHistoriaSerializer(serializers.Serializer):
    atributo = serializers.IntegerField(required = True)
    puntuacion = serializers.IntegerField(required = True)
    historia = serializers.IntegerField(required = True)

           
class AsignacionesResultantesPorHoras(object):
    def __init__( self, asignaciones = [], errores = [] ):
        self.asignaciones = asignaciones
        self.errores = errores


class AsignacionResultantePorHorasSerializer(serializers.Serializer):
    desarrollador = DesarrolladorSimpleSerializador()
    historias = HistoriaSimpleSerializador(many = True)

class AsignacionesResultantesPorHorasSerializer(serializers.Serializer):
    asignaciones = AsignacionResultantePorHorasSerializer ( many = True )
    errores = serializers.ListField( child = serializers.CharField())




class Desarrollador(object):
    """
    Almacena la informacion basica de un desarrollador
    """
    def fromKwargs(self, **kwargs):
        for field in ('id_externo', 'horasDisponiblesSemana'):
            setattr(self, field, kwargs.get(field, None))
    def __init__(self, id_externo=None, horasDisponiblesSemana=None):
        self.id_externo = id_externo
        self.horasDisponiblesSemana = horasDisponiblesSemana
    

class AsignacionResultantePorHoras:
    def __init__( self, desarrollador = None, historias = [] ):
        self.desarrollador = desarrollador
        self.historias = historias

desarrollador = Desarrollador(1,15)
historia = Historia(1,20)
historia_ = Historia(4,20)
historia__ = Historia(3,20)
asignacion_resultante = AsignacionResultantePorHoras(desarrollador, [historia, historia_, historia__])
asignacion_resultante_ = AsignacionResultantePorHoras(desarrollador, [historia, historia_, historia__])
asignaciones_resultantes = AsignacionesResultantesPorHoras([asignacion_resultante, asignacion_resultante_], ['hola ', 'hola'])
print (DesarrolladorSimpleSerializador(desarrollador).data)
print (AsignacionResultantePorHorasSerializer(asignacion_resultante).data)
print (AsignacionesResultantesPorHorasSerializer(asignaciones_resultantes).data)