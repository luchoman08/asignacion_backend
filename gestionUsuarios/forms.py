from django import forms
from .models import Usuario
from django.utils.translation import ugettext as _

class UsuarioForm (forms.ModelForm):
    confirm_password=forms.CharField(label = _('Confirmar contraseña'), widget=forms.PasswordInput(), max_length=100)
    password=forms.CharField(label = _('Contraseña'), widget=forms.PasswordInput(), max_length=100)
    class Meta:
        model = Usuario
        fields = ['username','email','password', 'confirm_password']
    def clean(self):
        cleaned_data = super(UsuarioForm, self).clean()
        password = cleaned_data.get("password")
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        if email and Usuario.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(_('Ya existe un usuario con ese correo.'))
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError(
                _('Las contraseñas deben coincidir')
            )        

class LoginForm(forms.Form):
    username = forms.CharField(label=_('Nombre de usuario'), max_length=100, required = True)
    password = forms.CharField(label =_('Contraseña'), max_length=100, widget=forms.PasswordInput(), required = True)
