from django.shortcuts import render
from .forms import AplicacionForm
from .models import Aplicacion
from gestionUsuarios import models as gestionUsuarios_models
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
# Create your views here.

@login_required
def adicionarAplicacion(request):
    if (Aplicacion.objects.filter(usuario__username=request.user.username).exists()):
        return redirect('verAplicacion')
    form = AplicacionForm(request.POST or None, request.FILES or None)
    adicion_exitosa = False
    if request.method == 'POST':
        if form.is_valid():
            aplicacion = form.save(commit=False)
            usuario = gestionUsuarios_models.Usuario.objects.get(username=request.user.username)
            aplicacion.usuario = usuario
            token, created = Token.objects.get_or_create(user=usuario)
            
            aplicacion.save()
            adicion_exitosa = True
    template = loader.get_template('gestionAplicaciones/gestionUsuarios/adicionarAplicacion.html')
    context = {'form': form, 'adicion_exitosa' : adicion_exitosa}
    return HttpResponse(template.render(context, request))
    
@login_required
def vistaAPI(request):
    template = loader.get_template('gestionAplicaciones/vistaAPI.html')
    return HttpResponse(template.render({}, request))
    
class DatosAplicacion(ListView):
    model = Aplicacion
    template_name = 'gestionAplicaciones/gestionUsuarios/verAplicacion.html'
    context_object_name = 'aplicacion'
    def get_queryset(self):
        try:
            return Aplicacion.objects.get(usuario__username=self.request.user.username)
        except Aplicacion.DoesNotExist:
            return None
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        token = '';
        try:
            token = Token.objects.get(user__username=self.request.user.username)
        except Token.DoesNotExist:
            token = _('No se ha generado token')
        context['token'] = token
        return context
    