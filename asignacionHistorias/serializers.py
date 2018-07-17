from rest_framework import serializers
from django.utils.translation import ugettext as _
from .models import Task, Agent
"""
Atributes
"""

class AtributoSerializer(serializers.Serializer):
    """
    Atributo o cualidad medible en un ente
    """
    id_externo = serializers.IntegerField(required=True)
    nombre = serializers.CharField(required = True)

"""
Puntuation 
"""
class PuntuacionAtributoSerializer(serializers.Serializer):
    id_atributo = serializers.IntegerField(required = True)
    puntuacion = serializers.IntegerField(required = True)

"""
Agents 
"""
class AgentSerializer(serializers.Serializer):
    external_id = serializers.CharField(required = True)
    capacity = serializers.IntegerField(required = True)

class AgentWithAttributesSerializer(serializers.Serializer):
    external_id = serializers.CharField(required = True)
    puntuaciones_atributos = PuntuacionAtributoSerializer(many=True, required = True)
"""
Tasks
"""

class TaskSerializer(serializers.Serializer):
    external_id = serializers.CharField(required = True)
    cost = serializers.FloatField(required = True)

class TaskWithAtributesSerializer(serializers.Serializer):
    external_id = serializers.CharField(required = True)
    puntuaciones_atributos = PuntuacionAtributoSerializer(many=True, required = True)

"""
Assignments input
"""


class AssignmentUniqueCostSerializer(serializers.Serializer):
    """
    Asignment based only in capacity of agents and unique cost in task 
    """
    agents =  AgentSerializer(many=True, required = True)
    tasks =  TaskSerializer(many=True, required = True)
    def get_tasks(self):
        tasks = self.validated_data.get('tasks')
        return [Task(**task) for task in tasks ]
    def get_agents(self):
        agents = self.validated_data.get('agents')
        return [Agent(**agent) for agent in agents ]
class AssignmentWithAttributesSerializer(serializers.Serializer):
    """
    Assignment with attributes and puntuation in each attribute for tasks and agents 
    """
    agents =  AgentWithAttributesSerializer(many=True, required = True)
    tasks =  TaskWithAtributesSerializer(many=True, required = True)
    def get_tasks(self):
        tasks = self.validated_data.get('tasks')
        return [Task(**task) for task in tasks ]
    def get_agents(self):
        agents = self.validated_data.get('agents')
        return [Agent(**agent) for agent in agents ]