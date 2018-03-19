from django.db import models
from django.utils.translation import ugettext as _
from modelosGenericos import models as modelos_genericos
# Create your models here.


class Atributo(models.Model):
    """
    Atributo o cualidad medible en un ente
    """
    id_externo = models.IntegerField(_('Id externo'), blank=False, null = False)
    nombre = models.CharField(_('Nombre del atributo'), max_length = 50, blank=True, null = True)
    descripcion = models.TextField(_('Descripcion del atributo'), max_length = 50, blank=False, null = False)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )
   

    
    
    
    
    
class AsignacionPorHoras(models.Model):
    relacion_horas_puntos = models.FloatField(_('Relacion horas-puntos'), blank =False, null =False)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )
   
   
class AsignacionPorCaracteristicas(models.Model):
    procurar_misma_cantidad_tareas = models.BooleanField(_('Procurar misma cantidad de tareas'), blank = False, null = False)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )

    
class Historia(models.Model):
    """
    Almacena una historia de usuario
    """
    id_externo = models.IntegerField(_('Id Externo'), blank=False, null=False) 
    puntuacionGeneral = models.IntegerField(_('Puntuacion general'), blank=False, null=False,default=0)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )
    asignacion_por_horas = models.ForeignKey(AsignacionPorHoras, on_delete = models.CASCADE);
    readonly_fields = ('fechaRegisro' )

class Desarrollador(models.Model):
    """
    Almacena la informacion basica de un desarrollador
    """
    id_externo = models.IntegerField(_('Id externo'), blank=False, null = False)
    horasDisponiblesSemana = models.IntegerField(_('Horas disponibles a la semana'), default = 0, blank=False)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )
    asignacion_por_horas = models.ForeignKey(AsignacionPorHoras, on_delete = models.CASCADE);
    readonly_fields=('fechaRegisro' )
    
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