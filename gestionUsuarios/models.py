from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
# Create your models here.


class Usuario(User):
    fecha_creacion = models.DateTimeField(_('Fecha de creaciòn del usuario'), null = False, auto_now_add = True, blank = True )