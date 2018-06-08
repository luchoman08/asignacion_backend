from rest_framework import serializers
from django.utils.translation import ugettext as _
from .models import Task, Agent



class AgentSerializer(serializers.Serializer):
    external_id = serializers.CharField(required = True)
    capacity = serializers.IntegerField(required = True)

class TaskSerializer(serializers.Serializer):
    external_id = serializers.CharField(required = True)
    cost = serializers.FloatField(required = True)

class AssignmentUniqueCostSerializer(serializers.Serializer):
    agents =  AgentSerializer(many=True, required = True)
    tasks =  TaskSerializer(many=True, required = True)
    def get_tasks(self):
        tasks = self.validated_data.get('tasks')
        return [Task(**task) for task in tasks ]
    def get_agents(self):
        agents = self.validated_data.get('agents')
        return [Agent(**agent) for agent in agents ]

