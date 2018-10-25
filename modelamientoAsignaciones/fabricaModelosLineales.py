from . import resolventes_genericos as resol_genericos
import re
import abc
import math
from collections import namedtuple
class BaseModelFactory:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def solve(self):
        """
        This method should be use the self properties and return the response of the linear algorithm in
        a readable format
        :return:
        """
        return


class BalancedModelFactory(BaseModelFactory):
    """
    Asignacion de tareas donde se busca que el porcentaje de utilizacion de los agentes
    sea lo mas balanceado posible (el porcentaje de utilizacion es el porcentaje de capacidad 
    asignado en cada agente con respecto a la capacidad total del agente )
    """

    def __init__(self, agents, tasks):
        """Init Balanced model factory
        
        Args:
            agents: {[list of deserialized Agents]} -- [See AgentSerializer]
            tasks {[list of deserialized Task]} -- [See TaskSerializer]
        """

        self.agents = agents
        self.tasks = tasks
        self.agents_capacities = {}
        self.tasks_costs = {}
        self.agents_capacities = {agent.external_id: agent.capacity for agent in self.agents }
        self.tasks_costs = {task.external_id: task.cost  for task in self.tasks }
    
    def solve(self):
        """Solve and returns the result by linear solver of task assignments
        
        Returns:
            [dict{assignments: dict{id_agent: [ids_task_assigned]}] -- [Assignments for agents]
        """

        pulp_status, pulp_variables = resol_genericos.solveEquilibriumProblem(self.agents_capacities, self.tasks_costs)
        assignments = {int(agent):[] for agent in self.agents_capacities.keys()}
        result = {}
        for variable in pulp_variables:
            numbers_in_var_name = re.findall(r'\d+', variable.name)
            if (len(numbers_in_var_name) == 2 and variable.varValue == 1):
                agent = int(numbers_in_var_name[0])
                task = int(numbers_in_var_name[1])
                assignments[agent].append(task)
        print(assignments)
        result['assignments'] = assignments
        return result


class AttributeBasedModelFactory(BaseModelFactory):
    """
    Fabrica de modelos donde se tienen en cuenta las habilidades de cada desarrollador (agent ) y
    los costos de cada historia (task) medidos por caracteristicas, podiendo mantener un equilibrio
    entre cantidad de historias asignadas o bien un minimo de historias asignadas a cada desarrollador
    """ 
    def __init__(self, agents, tasks, assign_same_quantity_of_tasks):
        """Generate a new Attribute based model factory

        Args:
            agents list of Agents]} -- [See AgentWithAttributesSerializer]
            tasks {[list of Tasks]} -- [See TaskWithAttributesSerializer]
            assign_same_quantity_of_tasks {[boolean]} -- [Say to solver y should include information to intent balance the number of task assigned]
        """
        self.agents = [resol_genericos.Agent(agent.external_id, {attribute.external_id: attribute.punctuation for attribute in agent.attributes_punctuation}) for agent in agents]
        self.tasks = [resol_genericos.Task(task.external_id, {attribute.external_id: attribute.punctuation for attribute in task.attributes_punctuation}) for task in tasks]
        self.assign_same_quantity_of_tasks = assign_same_quantity_of_tasks
        self.environment = resol_genericos.Environment(self.agents, self.tasks)  

    def solve(self):
        """Solve and returns the result by linear solver of task assignments with attributes
        
        Returns:
            [dict{assignments: dict{id_agent: [ids_task_assigned]}] -- [Assignments for agents]
        """      
        pulp_status, pulp_variables = resol_genericos.solveAttributesAssignmentProblem(self.environment, assign_same_quantity_of_tasks = self.assign_same_quantity_of_tasks  )
        asignaciones_resultado = {int(agent.id):[] for agent in self.agents}
        result = {}
        for variable in pulp_variables:
            numeros_en_nombre_variable = re.findall(r'\d+', variable.name)
            if len(numeros_en_nombre_variable) == 2 and variable.varValue == 1:
                agent = int(numeros_en_nombre_variable[0])
                task = int(numeros_en_nombre_variable[1])
                asignaciones_resultado[agent].append(task)
        print(asignaciones_resultado)
        result['assignments'] = asignaciones_resultado
        return result


class PairAssignmnentFactory(BaseModelFactory):
    """
    Asignación de tareas en donde se crea primero un emparejamiento de los desarrolladores y luego con base en dicho
    emparejamiento, se asignan las tareas por parejas
    """
    def __init__(self, agents, tasks, reverse):
        """
        Init pair assignment
        :param agents: list List of Agents
        :param reverse: bool Should be assigned the tasks
        """
        self.agents = [resol_genericos.Agent(agent.external_id, {attribute.external_id: attribute.punctuation for attribute in agent.attributes_punctuation}) for agent in agents]
        self.tasks = [resol_genericos.Task(task.external_id, {attribute.external_id: attribute.punctuation for attribute in task.attributes_punctuation}) for task in tasks]
        self.reverse = reverse

    def solve(self):
        """Solve and returns the result by linear solver of task assignments

        Returns:
            [dict{assignments: dict{id_agent: [ids_task_assigned]}] -- [Assignments for agents]
        """

        pulp_status, pulp_variables = resol_genericos.makePairs(self.agents,
                                                                self.reverse)
        Pair = namedtuple('Pair', ['first', 'second'], verbose=True)
        result = dict()
        pairs = list()
        for variable in pulp_variables:
            numbers_in_var_name = re.findall(r'\d+', variable.name)
            if len(numbers_in_var_name) == 2 and variable.varValue == 1:
                agent1 = int(numbers_in_var_name[0])
                agent2 = int(numbers_in_var_name[1])
                pairs.append(Pair(agent1, agent2))
        result['pairs'] = pairs
        return result

class TaskGroupModelFactory(BaseModelFactory):
    """
    Asignacion de tareas basada en agrupamiento de tareas, donde se busca
    que las asignaciones de cada agente sea lo mas homogenea posible con respecto 
    a los agrupamientos de las historias, por ejemplo, si se tienen dos agentes (a1, a2), 4 tareas
    (t1, t2, t3, t4) y dos grupos (g1 = [t1, t2], g2 = [t3, t4] se espera que las asignaciones 
    a a1 sean en su mayoria, pertenecientes al mismo grupo (sin importar cual) e igual sucede con las asignaciones al
    agente a2
    """

    def __init__(self, agents, tasks, groups):
        """Init task assignment
        
        Args:
            agents: {[list of deserialized Agents]} -- [See AgentSerializer]
            tasks: {[list of deserialized Task]} -- [See TaskSerializer]
            groups: {[list of deserialized TaskGroups] -- [See TaskGroupSerializer]}
        """

        self.agents = agents
        self.tasks = tasks
        self.groups = groups
        self.agents_capacities = {agent.external_id: agent.capacity for agent in self.agents }
        self.tasks_costs = {task.external_id: task.cost  for task in self.tasks }
        self.groups_dict = {group.external_id: group.task_ids for group in self.groups}

    def solve(self):
        """Solve and returns the result by linear solver of task assignments
        
        Returns:
            [dict{assignments: dict{id_agent: [ids_task_assigned]}] -- [Assignments for agents]
        """

        pulp_status, pulp_variables = resol_genericos.solveTaskGroupingAssignment(self.agents_capacities, self.tasks_costs, self.groups_dict)
        assignments = {int(agent):[] for agent in self.agents_capacities.keys()}
        result = {}
        for variable in pulp_variables:
            numbers_in_var_name = re.findall(r'\d+', variable.name)
            if len(numbers_in_var_name) == 2 and variable.varValue == 1:
                agent = int(numbers_in_var_name[0])
                task = int(numbers_in_var_name[1])
                assignments[agent].append(task)
        result['assignments'] = assignments
        return result