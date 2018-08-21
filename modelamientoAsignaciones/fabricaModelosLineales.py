from . import resolventes_genericos as resol_genericos
import pulp
import re

class BalancedModelFactory:
    """
    Balanced model factory and solver
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

class AttributeBasedModelFactory:
    """
    Fabrica de modelos donde se tienen en cuenta las habilidades de cada desarrollador (agent ) y
    los costos de cada historia (task) medidos por caracteristicas, podiendo mantener un equilibrio
    entre cantidad de historias asignadas o bien un minimo de historias asignadas a cada desarrollador
    """ 
    def __init__(self, agents, tasks, assign_same_quantity_of_tasks):
        """[summary]
        
        Arguments:
            agents {[list of Agents]} -- [See AgentWithAttributesSerializer]
            tasks {[list of Tasks]} -- [See TaskWithAttributesSerializer]
            assign_same_quantity_of_tasks {[boolean]} -- [Say to solver y should include information to intent balance the number of task assigned]
        """
        print(agents[0].attributes_punctuation)
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
            if (len(numeros_en_nombre_variable) == 2 and variable.varValue == 1):
                agent = int(numeros_en_nombre_variable[0])
                task = int(numeros_en_nombre_variable[1])
                asignaciones_resultado[agent].append(task)
        print(asignaciones_resultado)
        result['assignments'] = asignaciones_resultado
        return result
