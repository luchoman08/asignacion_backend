from django.db import models
from django.utils.translation import ugettext as _
from modelosGenericos import models as modelos_genericos
# Create your models here.


class Atributo(models.Model):
    """
    Atributo o cualidad medible en un ente
    """
    nombre = models.CharField(_('Nombre del atributo'), max_length = 50, blank=False, null = False)
    descripcion = models.TextField(_('Descripcion del atributo'), max_length = 50, blank=False, null = False)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )
"""   
class HistoriaConAtributos(modelos_genericos.Historia):
    atributos = models.ManyToManyField(
        Atributo,
        through='PuntuacionAtributoHistoria',
        through_fields=('historia', 'atributo'),
        related_name='HistoriarAsignacionAtributos' )

class DesarrolladorConAtributos(modelos_genericos.Desarrollador):
    atributos = models.ManyToManyField(
        Atributo,
        through='PuntuacionAtributoDesarrollador',
        through_fields=('desarrollador', 'atributo'),
        related_name='DesarrolladorAsignacionAtributos')
    

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