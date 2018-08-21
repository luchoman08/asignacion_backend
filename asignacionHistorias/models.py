from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.

    
class AtributePunctuation(models.Model):
    def __init__(self, external_id = None, punctuation = None):
        self.external_id = external_id
        self.punctuation = punctuation

class Task(models.Model):
    external_id = models.IntegerField(_('External ID'), blank=False, null=False)
    cost = models.IntegerField(_('Cost'), blank=False, null=False,default=0)

class TaskWithAttributes(object):
    def fromKwargs(self, **kwargs):
        for field in ('external_id', 'attributes_punctuation', ):
            setattr(self, field, kwargs.get(field, None))
    def __init__(self, external_id = None, attributes_punctuation = None):
        """[summary]
        
        Arguments:
            external_id {[string]} -- [Id than referer to actual task in external app] (default: {None})
            attributes_punctuation {[list of AtributePunctuation]} -- [Atribute punctuations assigned] (default: {None})
        """
        self.external_id = external_id
        self.attributes_punctuation = [AtributePunctuation(**attribute_punctuation) for attribute_punctuation in attributes_punctuation]


class Agent(object):
    def fromKwargs(self, **kwargs):
        for field in ('external_id', 'capacity', ):
            setattr(self, field, kwargs.get(field, None))
    def __init__(self, external_id=None, capacity=None):
        self.external_id = external_id
        self.capacity = capacity

class AgentWithAttributes(Agent):
    def fromKwargs(self, **kwargs):
        for field in ('external_id', 'attributes_punctuation', ):
            setattr(self, field, kwargs.get(field, None))
    def __init__(self, external_id=None, attributes_punctuation=None):
        self.external_id = external_id
        self.attributes_punctuation =  [AtributePunctuation(**attribute_punctuation) for attribute_punctuation in attributes_punctuation]    
class AssignmentUniqueCost(object):
    def __init__(self, tasks=None, agents=None):
        self.tasks = tasks
        self.agents = agents

