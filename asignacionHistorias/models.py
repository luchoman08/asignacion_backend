from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.

    


class Task(models.Model):
    external_id = models.IntegerField(_('External ID'), blank=False, null=False)
    cost = models.IntegerField(_('Cost'), blank=False, null=False,default=0)


class Agent(object):
    def fromKwargs(self, **kwargs):
        for field in ('external_id', 'capacity', ):
            setattr(self, field, kwargs.get(field, None))
    def __init__(self, external_id=None, capacity=None):
        self.external_id = external_id
        self.capacity = capacity
    
class AssignmentUnique(object):
    def __init__(self, tasks=None, agents=None):
        self.tasks = tasks
        self.agents = agents

