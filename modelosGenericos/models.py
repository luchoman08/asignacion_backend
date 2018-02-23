from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.

class Proyecto(models.Model):
    nombre = models.CharField(_('Nombre'), max_length = 50, blank=False, null = False)
    fechaInicio =  models.DateTimeField(_('Fecha de inicio'), null = False)
    fechaFinalizacion =  models.DateTimeField(_('Fecha de finalizacion'), null = True)
    """
    Cada punto se debe multiplicar por su correspondencia en horas
    ej: correspondencia = 2, puntos = 0.5, horas = 2*0.5
    """

class Historia(models.Model):
    """
    Almacena una historia de usuario
    """
    nombre = models.CharField(_('Nombre de historia de usuario'), max_length=50, blank=False, null=False) 
    descripcion = models.CharField(_('Descripcion de la historia de usuario'), max_length=150, blank=False, null=False)
    puntuacionGeneral = models.IntegerField(_('Puntuacion general'), blank=False, null=False,default=0)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )
    fechaMoficacion = models.DateTimeField(_('Fecha de modificacion'), auto_now=False, null = True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    readonly_fields=('fechaRegisro' )

class Desarrollador(models.Model):
    """
    Almacena la informacion basica de un desarrollador
    """
    nombre = models.CharField(_('Nombre del desarrollador'), max_length = 50, blank=False, null = False)
    horasDisponiblesSemana = models.IntegerField(_('Horas disponibles a la semana'), default = 0)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )
    fechaMoficacion = models.DateTimeField(_('Fecha de modificacion'), auto_now=False, null = True)
    readonly_fields=('fechaRegisro' )

#many to many desarrollador a proyecto


    
    
#class Iteracion(models.model):

class ProyectoAgil(Proyecto):
    correspondenciaPuntosHoras = models.DecimalField(_('Correspondencia puntos horas proyecto'), max_digits = 50, decimal_places = 2, null = False)