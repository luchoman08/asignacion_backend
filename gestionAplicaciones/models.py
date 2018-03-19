from django.db import models
from gestionUsuarios import models as gestionUsuarios_models
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext as _
# Create your models here.
class Aplicacion(models.Model):
    """
    Almacena la información de las aplicaciones
    """
    nombre = models.CharField(_('Nombre de la Aplicación'), max_length=50, blank=False, null=False) 
    url = models.URLField(_('URL de la Aplicación'), max_length=50, blank=False, null=False, unique = True) 
    descripcion = models.TextField(_('Resumen de la aplicacion'), max_length=50, blank=False, null=False)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )
    fechaMoficacion = models.DateTimeField(_('Fecha de modificacion'), auto_now=False, null = True)
    usuario = models.OneToOneField(gestionUsuarios_models.Usuario, on_delete=models.CASCADE)
    readonly_fields=('fechaRegisro')
    
    def token_generado(self):
        try:
            token = Token.objects.get(user=self.usuario)
            return True
        except Token.DoesNotExist:
            return False
