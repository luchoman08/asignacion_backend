from django import forms
from .models import Aplicacion
from django.utils.translation import ugettext as _


class AplicacionForm (forms.ModelForm):
    class Meta:
        model = Aplicacion
        fields = ['nombre','url','descripcion']
"""        
    nombre = models.CharField(_('Nombre de la Aplicación'), max_length=50, blank=False, null=False) 
    url = models.CharField(_('URL de la Aplicación'), max_length=50, blank=False, null=False) 
    descripcion = models.TextField(_('Resumen de la aplicacion'), max_length=50, blank=False, null=False)
    fechaRegistro = models.DateTimeField(_('Fecha de registro'), auto_now=True )
    fechaMoficacion = models.DateTimeField(_('Fecha de modificacion'), auto_now=False, null = True)
    usuario = models.OneToOneField(gestionUsuarios_models.Usuario, on_delete=models.CASCADE)
    readonly_fields=('fechaRegisro' )
    
"""