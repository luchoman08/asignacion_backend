from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.


class Atributo(models.Model):
    """
    Atributo o cualidad medible en un ente
    """
    id_externo = models.IntegerField(_('Id externo'), blank=False, null = False)
    nombre = models.CharField(_('Nombre del atributo'), max_length = 50, blank=True, null = True)
    descripcion = models.TextField(_('Descripcion del atributo'), max_length = 50, blank=False, null = False)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )
   
    
    
class AsignacionPorHoras(object):
    def __init__(self, historias = [], desarrolladores = [], relacion_horas_puntos = None ):
        self.historias = historias
        self.desarrolladores = desarrolladores
        self.relacion_horas_puntos = relacion_horas_puntos
    
class Historia(models.Model):
    """
    Almacena una historia de usuario
    """
    id_externo = models.IntegerField(_('Id Externo'), blank=False, null=False)
    descripcion = models.CharField(_('Descripcion'), blank=True, null=True, max_length = 250)
    puntuacionGeneral = models.IntegerField(_('Puntuacion general'), blank=False, null=False,default=0)



class Desarrollador(object):
    """
    Almacena la informacion basica de un desarrollador
    """
    def fromKwargs(self, **kwargs):
        for field in ('id_externo', 'nombre', 'horasDisponiblesSemana'):
            setattr(self, field, kwargs.get(field, None))
    def __init__(self, id_externo=None, nombre=None, horasDisponiblesSemana=None):
        self.id_externo = id_externo
        self.nombre = nombre
        self.horasDisponiblesSemana = horasDisponiblesSemana
    

class AsignacionResultantePorHoras(object):
    def __init__( self, desarrollador = None, historias = [] ):
        self.desarrollador = desarrollador
        self.historias = historias

class AsignacionesResultantesPorHoras(object):
    def __init__( self, asignaciones = [], errores = [] ):
        self.asignaciones = asignaciones
        self.errores = errores
   
class AsignacionPorCaracteristicas(models.Model):
    procurar_misma_cantidad_tareas = models.BooleanField(_('Procurar misma cantidad de tareas'), blank = False, null = False)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )

class GrupoHistoriasRelacionadas(models.Model):
    """
    Grupo de historias que se asume estan relacionadas entre si
    """
    id_externo =  models.IntegerField(_('Id Externo'), blank=False, null=False) 
    historias = models.ManyToManyField(Historia)

class AsignacionPorCaracteristicasYGrupos(models.Model):
    procurar_misma_cantidad_tareas = models.BooleanField(_('Procurar misma cantidad de tareas'), blank = False, null = False)
    grupos_historias = models.ManyToManyField(GrupoHistoriasRelacionadas)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )
    

    
class DesarrolladorConAtributos(models.Model):
    """
    Almacena la informacion basica de un desarrollador
    """
    id_externo = models.IntegerField(_('Id externo'), blank=False, null = False)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )
    #asignacion_por_caracteristicas = models.ForeignKey(AsignacionPorCaracteristicas, on_delete = models.CASCADE);
    readonly_fields=('fechaRegisro' )
    atributos = models.ManyToManyField(
        Atributo,
        through='PuntuacionAtributoDesarrollador',
        through_fields=('desarrollador', 'atributo'),
        related_name='DesarrolladorAsignacionAtributos', null = True)
        
class HistoriaConAtributos(models.Model):
    id_externo = models.IntegerField(_('Id Externo'), blank=False, null=False) 
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True , null = True)
    #asignacion_por_caracteristicas = models.ForeignKey(AsignacionPorCaracteristicas, on_delete = models.CASCADE);
    readonly_fields = ('fechaRegisro' )
    atributos = models.ManyToManyField(
        Atributo,
        through='PuntuacionAtributoHistoria',
        through_fields=('historia', 'atributo'),
        related_name='HistoriarAsignacionAtributos' )

class PuntuacionAtributoDesarrollador(models.Model):

    desarrollador = models.ForeignKey(DesarrolladorConAtributos, on_delete=models.CASCADE, related_name='puntuacion_desarrollador')
    atributo = models.ForeignKey(Atributo, on_delete=models.CASCADE, related_name='puntuacion_desarrollador')
    puntuacion = models.DecimalField(_('Puntuacion'), max_digits=9, decimal_places=3)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )

class PuntuacionAtributoHistoria(models.Model):
    historia = models.ForeignKey(HistoriaConAtributos, on_delete=models.CASCADE, related_name='puntuacion_historia')
    atributo = models.ForeignKey(Atributo, on_delete=models.CASCADE, related_name='puntuacion_historia')
    puntuacion = models.DecimalField(_('Puntuacion'), max_digits=9, decimal_places=3)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )





"""    
class AsignacionPorHoras:
    Asignación simple de tareas donde solo se tiene en cuenta las horas que 
    tardara cada historia y las horas disponibles por usuario
    
    Parameters
    ----------
        historias: `list`
            Lista de historias (instancias de ``Historia``)
        desarrolladores: `list`
            Lista de desarrolladores (instancias de ``Desarrolladores``)
        relacion_horas_puntos: `float`
            Cantidad por la que se debera multiplicar cada punto para saber
            un estimado de cuantas horas tardara la realización de la historia
            por cada punto

    
    def __init__(self, historias, desarrolladores, relacion_horas_puntos):
        self.historias = historias
        self.desarrolladores = desarrolladores
        self.relacion_horas_puntos = relacion_horas_puntos
"""