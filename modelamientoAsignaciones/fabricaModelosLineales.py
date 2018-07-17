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
            [dict{id_agent: [ids_task_assigned]}] -- [Assignments for agents]
        """

        pulp_status, pulp_variables = resol_genericos.solveEquilibriumProblem(self.agents_capacities, self.tasks_costs)
        assignments = {int(agent):[] for agent in self.agents_capacities.keys()}
        
        for variable in pulp_variables:
            numbers_in_var_name = re.findall(r'\d+', variable.name)
            if (len(numbers_in_var_name) == 2 and variable.varValue == 1):
                agent = int(numbers_in_var_name[0])
                task = int(numbers_in_var_name[1])
                assignments[agent].append(task)
        print(assignments)
        return assignments

class AttributeBasedModelFactory:
    """
    Fabrica de modelos donde se tienen en cuenta las habilidades de cada desarrollador (agente ) y
    los costos de cada historia (tarea) medidos por caracteristicas, podiendo mantener un equilibrio
    entre cantidad de historias asignadas o bien un minimo de historias asignadas a cada desarrollador
    """ 
    

    def __init__(self, agents, tasks, assign_same_quantity_of_tasks):
        """[summary]
        
        Arguments:
            agents {[list of deserialized Agents]} -- [See AgentWithAttributesSerializer]
            tasks {[type]} -- [description]
            assign_same_quantity_of_tasks {[boolean]} -- [Say to solver y should include information to intent balance the number of task assigned]
        """

        #self.puntuacion_atributos_tarea = puntuacion_atributos_tarea
        #self.puntuacion_atributos_agente = puntuacion_atributos_agente
        #puntuacion_atributos_agente_dict = self.getpuntuacion_atributos_agente_dict(agents)
        #puntuacion_atributos_tarea_dict = self.getpuntuacion_atributos_tarea_dict(tasks)
        self.agents = [resol_genericos.Agente(agente.id_externo, puntuacion_atributos_agente_dict[agente.id_externo]) for agente in agents]
        self.tasks = [resol_genericos.Tarea(tarea.id_externo, puntuacion_atributos_tarea_dict[tarea.id_externo]) for tarea in tasks]
        self.caracteristicas = caracteristicas
        self.assign_same_quantity_of_tasks = assign_same_quantity_of_tasks
        self.entorno = resol_genericos.Entorno(self.agents, self.tasks, self.caracteristicas)       
    def solve(self):
        
        pulp_status, pulp_variables = resol_genericos.resolverProblemaEquilibrioConHabilidades(self.entorno, assign_same_quantity_of_tasks = self.assign_same_quantity_of_tasks  )
        asignaciones_resultado = {int(agente.id):[] for agente in self.agents}
        
        for variable in pulp_variables:
            numeros_en_nombre_variable = re.findall(r'\d+', variable.name)
            if (len(numeros_en_nombre_variable) == 2 and variable.varValue == 1):
                agente = int(numeros_en_nombre_variable[0])
                tarea = int(numeros_en_nombre_variable[1])
                asignaciones_resultado[agente].append(tarea)
        print(asignaciones_resultado)
        return asignaciones_resultado
