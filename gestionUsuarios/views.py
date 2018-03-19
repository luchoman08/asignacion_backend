from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Usuario
from .forms import UsuarioForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.shortcuts import redirect

# Create your views here.

@login_required
def index(request):
    template = loader.get_template('gestionUsuarios/index.html')
    context = { }
    return HttpResponse(template.render(context, request))
    
def crearUsuarios(request):
    form = UsuarioForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('signin')
    template = loader.get_template('gestionUsuarios/signup.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))

def logout_view(request):
    logout(request)
    request.session['just_logged_out'] = True
    return redirect('signin')
    


def loginInterno(request):
    form = LoginForm(request.POST or None, request.FILES or None)
    error = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('gestionUsuariosIndex')
        else:
            error = True
    
    try:
        just_logged_out = request.session.get('just_logged_out',False)
    except:
        just_logged_out = False
    template = loader.get_template('gestionUsuarios/signin.html')
    context = {'form': form, 'error': error, 'desde_logout': just_logged_out}
    request.session['just_logged_out'] = False
    return HttpResponse(template.render(context, request))    
    