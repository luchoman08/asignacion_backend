from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.

    
class AtributePunctuation(models.Model):
    def __init__(self, external_id = None, punctuation = None):
        self.external_id = external_id
        self.punctuation = punctuation

class Task(models.Model):
    external_id = models.IntegerField(_('External ID'), blank=False, null=False)
    cost = models.FloatField(_('Cost'), blank=False, null=False, default=0, max_length=200)


class TaskGroup(object):

    def fromKwargs(self, **kwargs):
        for field in ('external_id', 'task_ids', ):
            setattr(self, field, kwargs.get(field, None))

    def __init__(self, external_id = None, task_ids = None):
        """Group of tasks
        
        Arguments:
            external_id {[string]} -- External id of task group  (default: {None})
            tasks_ids {[list of int]} -- List of task ids than compound the group (default: {None})
        """
        self.external_id = external_id
        self.task_ids = task_ids 

class TaskWithAttributes(object):

    def fromKwargs(self, **kwargs):
        for field in ('external_id', 'attributes_punctuation', ):
            setattr(self, field, kwargs.get(field, None))

    def __init__(self, external_id = None, attributes_punctuation = None):
        """Task with attributes than explain how to hard is the task based in punctuations over attributes
        
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


class AgentPair(object):

    def fromKwargs(self, **kwargs):
        for field in('agent1', 'agent2',):
            setattr(self, field, kwargs.get(field, None))

    def __init__(self, agent1=None, agent2=None):
        self.agent1 = agent1
        self.agent2 = agent2


class AssignmentUniqueCost(object):

    def __init__(self, tasks=None, agents=None):
        self.tasks = tasks
        self.agents = agents

