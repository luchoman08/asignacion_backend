from rest_framework import serializers
from .models import Task, Agent, AgentWithAttributes, TaskWithAttributes, TaskGroup, AgentPair

"""
Punctuation 
"""


class AtributePunctuation(serializers.Serializer):
    external_id = serializers.CharField(required=True) # External id of attribute
    punctuation = serializers.FloatField(required=True)


"""
Agents 
"""


class AgentSerializer(serializers.Serializer):
    external_id = serializers.CharField(required=True)
    capacity = serializers.FloatField(required=True)


class AgentWithAttributesSerializer(serializers.Serializer):
    external_id = serializers.CharField(required=True)
    attributes_punctuation = AtributePunctuation(many=True, required=True)


class AgentPairSerializer(serializers.Serializer):
    agent1 = AgentWithAttributesSerializer(required=True)
    agent2 = AgentWithAttributesSerializer(required=True)


"""
Tasks
"""


class TaskSerializer(serializers.Serializer):
    external_id = serializers.CharField(required = True)
    cost = serializers.FloatField(required = True)


class TaskWithAtributesSerializer(serializers.Serializer):
    external_id = serializers.CharField(required = True)
    attributes_punctuation = AtributePunctuation(many=True, required = True)


class TaskGroupSerializer(serializers.Serializer):
    external_id = serializers.CharField(required = True)
    task_ids = serializers.ListField(child=serializers.CharField(required = True), required=True)


"""
Assignments input
"""


class AssignmentWithPairsSerializer(serializers.Serializer):
    """
    Assignment based in multiple attributes and punctuations made to a generated pairs of developers
    """
    agents = AgentWithAttributesSerializer(many=True, required=True)
    tasks = TaskWithAtributesSerializer(many=True, required=True)
    reverse = serializers.BooleanField(required=False, default=False)

    def get_agents(self):
        agents = self.validated_data.get('agents')
        return [AgentWithAttributes(**agent) for agent in agents]

    def get_tasks(self):
        tasks = self.validated_data.get('tasks')
        return [TaskWithAttributes(**task) for task in tasks]

    def get_reverse(self):
        return self.validated_data.get('reverse')


class AssignmentUniqueCostSerializer(serializers.Serializer):
    """
    Assignment based only in capacity of agents and unique cost in task
    """
    agents = AgentSerializer(many=True, required = True)
    tasks = TaskSerializer(many=True, required = True)

    def get_tasks(self):
        tasks = self.validated_data.get('tasks')
        return [Task(**task) for task in tasks ]

    def get_agents(self):
        agents = self.validated_data.get('agents')
        return [Agent(**agent) for agent in agents]


class AssignmentWithAttributesSerializer(serializers.Serializer):
    """
    Assignment with attributes and puntuation in each attribute for tasks and agents 
    """
    agents =  AgentWithAttributesSerializer(many=True, required = True)
    tasks =  TaskWithAtributesSerializer(many=True, required = True)
    assign_same_quantity_of_tasks = serializers.BooleanField(required = True)

    def get_assign_same_quantity_of_tasks(self):
        return self.validated_data.get('assign_same_quantity_of_tasks')

    def get_tasks(self):
        tasks = self.validated_data.get('tasks')
        return [TaskWithAttributes(**task) for task in tasks]

    def get_agents(self):
        agents = self.validated_data.get('agents')
        return [AgentWithAttributes(**agent) for agent in agents]


class AssignmentWithGroupsSerializer(serializers.Serializer):
    """
    Assignment with attributes and puntuation in each attribute for tasks and agents 
    """
    agents =  AgentSerializer(many=True, required = True)
    tasks =  TaskSerializer(many=True, required = True)
    groups = TaskGroupSerializer(many=True)
    assign_same_quantity_of_tasks = serializers.BooleanField(required = True)

    def get_assign_same_quantity_of_tasks(self):
        return self.validated_data.get('assign_same_quantity_of_tasks')

    def get_tasks(self):
        tasks = self.validated_data.get('tasks')
        return [Task(**task) for task in tasks]

    def get_agents(self):
        agents = self.validated_data.get('agents')
        return [Agent(**agent) for agent in agents]

    def get_groups(self):
        groups = self.validated_data.get('groups')
        return [TaskGroup(**group) for group in groups]