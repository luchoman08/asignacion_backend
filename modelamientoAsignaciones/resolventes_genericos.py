import itertools, string, re
from pulp import *
from time import time
import math
import numbers
import sys
from functools import reduce
from collections import namedtuple

Pair = namedtuple('Pair', ['first', 'second'], verbose=True)

class Task:

    def __init__(self, id, costo_caracteristica):
        self.id = id
        self.costo_caracteristica = costo_caracteristica  # dict

costo_caracteristica = dict()
costo_caracteristica[1] = 0
costo_caracteristica[2] = 10
costo_caracteristica[3] = 0
costo_caracteristica_ = dict()
costo_caracteristica_[1] = 10
costo_caracteristica_[2] = 0
costo_caracteristica_[3] = 0
task = Task(1, costo_caracteristica)
tarea_ = Task(2, costo_caracteristica_)


class Agent:
    DEFAULT_ID = '11111111111111'
    DEFAULT_SKILL_ID = -1
    MINIMUM_SKILL_VALUE = 1

    def __init__(self, id, skills):
        """
        Init Agent
        :param id: string Unique id for Agent
        :param skills: dict The keys are the skills id and value is numeric value for the skill
        """
        self.id = id
        self.skills = skills  # dict

    @staticmethod
    def get_standard_agent(agents, id = None):

        """Retorna un agente cuyas skills son la media de un grupo de agentes, debe haber almenos un agente,
        el id de este agente sera DEFAULT_ID
        Args:
            agents: list of Agent
        Returns:
            agent: instance of Agent
        """
        _id = id
        if not _id:
            _id = Agent.DEFAULT_ID
        if len(agents) <= 0:
            raise ValueError('Debe ingresar almenos un agente')
        elif len(agents) == 1:
            return Agent(_id, agents[0].skills)

        id_skills = agents[0].skills.keys()
        cantidad_agentes = len(agents)
        skills_media = {id_habilidad: None for id_habilidad in id_skills}
        for id_habilidad in id_skills:
            skills_media[id_habilidad] = reduce((lambda x, y: x + y),
                                                [agent.skills[id_habilidad] for agent in agents]) / float(
                cantidad_agentes)
        return Agent(_id, skills_media)

    @staticmethod
    def get_little_skillful_agent(id_skills, str_id=False):
        """Retorna un agente con las skills mas bajas posibles

        :param id_skills: list of integer
        :param str_id: bool True if the default id should be returned as string format
        :return little_skillful_agent: Agent
        """
        skills = {id_skill: Agent.MINIMUM_SKILL_VALUE for id_skill in id_skills}
        agent_id = Agent.DEFAULT_ID if not str_id else str(Agent.DEFAULT_ID)
        return Agent(agent_id, skills)

    @staticmethod
    def get_compatibility(agent1, agent2):
        def compatibility_func(habilidad1, habilidad2):
            max_val = max(habilidad1, habilidad2)
            if max_val == 0:
                max_val = 1
            return min(habilidad1, habilidad2) * 100 / max_val
        """Retorna la compatibilidad del 1 al 100 la cual indica que tan compatibles son dos agentes

        :param agent1: Agent
        :param agent2: Agent

        :return compatibility: int Agent compatibility, the returned value is beween 1 and 100, where at major
            returned value major compatibility

        """
        compatibility = 0
        id_skills = agent1.skills.keys()
        cantidad_skills = len(id_skills)
        porcentaje_importancia_por_habilidad = 1 / float(cantidad_skills)
        for id_habilidad in id_skills:
            compatibility += porcentaje_importancia_por_habilidad * compatibility_func(agent1.skills[id_habilidad],
                                                                                       agent2.skills[id_habilidad])
        return compatibility

skills = dict()
skills[1] = 10
skills[2] = 1
skills[3] = 1
skill_ = dict()
skill_[1] = 1
skill_[2] = 10
skill_[3] = 1
agent = Agent(1, skills)
agente_ = Agent(2, skill_)


class Environment:

    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks
        self.costos = {}
        self.agents_dict = {agent.id: agent for agent in agents}
        self.tasks_dict = {task.id: task for task in tasks}
        self.agents_x_tasks = list(itertools.product(self.agents_dict.keys(), self.tasks_dict.keys()))
        self.init_cost()

    def init_cost(self):
        for agentextarea in self.agents_x_tasks:
            self.costos[agentextarea] = self.get_cost(self.agents_dict[agentextarea[0]],
                                                      self.tasks_dict[agentextarea[1]])

    def get_cost(self, agent, task):
        cost = 0
        for id_caracteristica in task.costo_caracteristica.keys():
            # La habilidad caracteristica no puede ser 0 dado que se usa en una división, para este modelo el minimo de habilidad es 0.1, por ende para prevenir errores se normaliza esta propiedad
            skill_normalizada = agent.skills[id_caracteristica] if isinstance(
                agent.skills[id_caracteristica], numbers.Number) and agent.skills[
                                                                                                            id_caracteristica] != 0 else 0.1
            cost += task.costo_caracteristica[id_caracteristica] * task.costo_caracteristica[
                id_caracteristica] / skill_normalizada
        return cost


class GrupoHistorias:
    """Grupo de historias
    """

    def __init__(self, id_grupo, ids):
        """Creacion de un nuevo grupo de historias

        :param id_grupo: string Id unico de grupo
        :param ids: list Lista de ids de las historias que conforman el grupo
        """
        self.id_grupo = id_grupo
        self.ids = ids


class EntornoConGruposHistorias:

    def __init__(self, agents, tasks, grupo_tareas, caracteristicas):
        self.agents = agents
        self.grupo_tareas = grupo_tareas
        self.tasks = tasks
        self.caracteristicas = caracteristicas  # dict
        self.costos = {}
        self.costos_grupo = {}
        self.agents_dict = {agent.id: agent for agent in agents}
        self.tasks_dict = {task.id: task for task in tasks}
        self.relaciones_tareas_dict = {grupo_tarea['id_externo']: grupo_tarea['id_historias'] for grupo_tarea in
                                       self.grupo_tareas}
        self.agents_x_tasks = list(itertools.product(self.agents_dict.keys(), self.tasks_dict.keys()))
        self.agentesxrelaciones_tareas = list(
            itertools.product(self.agents_dict.keys(), self.relaciones_tareas_dict.keys()))
        self.init_cost()
        self.init_costos_grupo()

    def get_cost(self, agent, task):
        cost = 0
        for id_caracteristica in task.costo_caracteristica.keys():
            cost += task.costo_caracteristica[id_caracteristica] * task.costo_caracteristica[id_caracteristica] / \
                    agent.skills[id_caracteristica]
        return cost

    def costoGrupoTareas(self, id_tareas, agent):
        resultado = 0
        for id_tarea in id_tareas:
            resultado += self.get_cost(agent, self.tasks_dict[id_tarea])
        return resultado

    def init_cost(self):
        for agentextarea in self.agents_x_tasks:
            self.costos[agentextarea] = self.get_cost(self.agents_dict[agentextarea[0]],
                                                      self.tasks_dict[agentextarea[1]])

    def init_costos_grupo(self):
        for agentexrelacion_tareas in self.agentesxrelaciones_tareas:
            self.costos_grupo[agentexrelacion_tareas] = self.costoGrupoTareas(
                self.relaciones_tareas_dict[agentexrelacion_tareas[1]], self.agents_dict[agentexrelacion_tareas[0]])


agents = [agent, agente_]
tasks = [task, tarea_]
environment = Environment(agents, tasks)


def solveAttributesAssignmentProblem(environment, assign_same_quantity_of_tasks=False):
    """Resuelve el problema de la asignacion garantizando un equilibrio en las cargas asignadas, adicionando
    puntuacion de el agent en caracteristicas especificas y costos en las tasks .

    La escala de habilidades_caracteristica es del 0 al 10
    La escala de costo_caracteristica es del 0 al 10
    Se asignan las tasks de tal forma que se minimize la diferencia de cargas asignadas, en
    porcentaje con respecto al cost basado en que tanto le cuesta a cada agent hacer sus asignaciones,
    dependiendo sus habilidades y el cost definido en distintos argumentos de la task

    Args:
        agents (list of ´´Agente´´): Agentes a asignar
        tasks (list of ´´Tarea´´): Tareas a asignar
    Returns:
        (status, list): (Estado de el solver pulp, Lista de variables pulp con sus resultados)


    """
    prob = LpProblem("Equilibrio de asignaciones", LpMinimize)
    variables_asignacion = LpVariable.dicts("Asignacion", environment.agents_x_tasks, None, None, LpBinary)

    # Funcion objetivo

    prob += lpSum([environment.costos[agentextarea] * variables_asignacion[agentextarea] for agentextarea in
                   environment.agents_x_tasks])
    # Una task solamente puede ser asignada a una persona:

    for task in environment.tasks:
        prob += lpSum([variables_asignacion[agentextarea] for agentextarea in environment.agents_x_tasks if
                       agentextarea[1] == task.id]) == 1

    if assign_same_quantity_of_tasks:

        minimas_tareas = math.floor(len(environment.tasks) / len(environment.agents))
        for agent in environment.agents:
            prob += lpSum([variables_asignacion[agentextarea] for agentextarea in environment.agents_x_tasks if
                           agentextarea[0] == agent.id]) >= minimas_tareas

    prob.writeLP("EquilibrioConHabilidades.lp")
    tiempo_solve_inicial = time()
    prob.solve()
    tiempo_final_solve = time()

    tiempo_solve = tiempo_final_solve - tiempo_solve_inicial

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    for v in prob.variables():
        print(v.name, "=", v.varValue)
    print('El tiempo total de el solve fue:', tiempo_solve)  # En segundos
    return prob.status, prob.variables()


solveAttributesAssignmentProblem(environment, assign_same_quantity_of_tasks=True)


def solveEquilibriumProblem(agente_capacidad, tarea_costo, knowing_minimum=0, knowing_maximum=sys.maxsize, maxtime=sys.maxsize):
    """Resuelve el problema de la asignación garantizando un equilibrio en las cargas asignadas.

    Se asignan las tasks de tal forma que se minimize la diferencia de cargas asignadas, en
    porcentaje con respecto a la capacidad disponibles por cada agent

    Args:
        agente_capacidad (dict of str: int): Identificacion de el agent como llave, la capacidad es el valor.
        tarea_costo (dict of str: int): Identificacion de la task como llave, su cost es el valor.
        maxtime Tiempo maximo de ejecución de el solver

    Returns:
        (status, list): (Estado de el solver pulp, Lista de variables pulp con sus resultados)


    """
    agents = agente_capacidad.keys()
    tasks = tarea_costo.keys()
    agents_x_tasks = list(itertools.product(agente_capacidad.keys(),
                                            tarea_costo.keys()))  # Lista de pares resultante de hacer producto cartesiano entre agents y tasks
    prob = LpProblem("Equilibrio de asignaciones", LpMinimize)
    variables_asignacion = LpVariable.dicts("Asignacion", agents_x_tasks, None, None, LpBinary)
    # Variables auxiliares para ayudarse a resolver la desviacin estandard
    aux_vars = LpVariable.dicts("Auxiliar", [(a, "temporal") for a in agents], None, None)
    promedio_porcentaje = LpVariable('promedio_porcentaje', None, None, LpContinuous)
    # Funcion objetivo

    def construir_funcion_objetivo(agents):
        return lpSum(aux_vars)

    prob += construir_funcion_objetivo(agents), "Minimizar desviacion estandard de el trabajo"

    porcentaje_uso_tiempo_agentes = {}
    cargas_por_agente = {}

    for agent in agents:
        cargas_por_agente[agent] = [tarea_costo[i[1]] * variables_asignacion[i] for i in agents_x_tasks if
                                    i[0] == agent]

    for agent in agents:
        porcentaje_uso_tiempo_agentes[agent] = lpSum(
            [x * 100 / agente_capacidad[agent] for x in cargas_por_agente[agent]])

    promedio_porcentaje_uso_tiempo_agentes_exepto_agente = {}

    porcentaje_uso_tiempo_agentes_menos_porcentaje_uso_tiempo_agente_dividido_longitud_agentes = {}
    for agent in agents:
        porcentaje_uso_tiempo_agentes_menos_porcentaje_uso_tiempo_agente_dividido_longitud_agentes[agent] = \
        porcentaje_uso_tiempo_agentes[agent] - porcentaje_uso_tiempo_agentes[agent] / float(len(agents))

    for agent in agents:
        promedio_porcentaje_uso_tiempo_agentes_exepto_agente[agent] = \
            (-lpSum([porcentaje_uso_tiempo_agentes[agentex]
                     for agentex in agents if agentex != agent]) / float(len(agents))) + \
            porcentaje_uso_tiempo_agentes_menos_porcentaje_uso_tiempo_agente_dividido_longitud_agentes[agent]

    # Restricciones

    # La suma de las horas asignadas no puede superar el mximo de horas disponibles
    for agent in agents:
        prob += lpSum(cargas_por_agente[agent]) <= agente_capacidad[agent]

    # Una task solamente puede ser asignada a una persona:

    for task in tasks:
        prob += lpSum([variables_asignacion[i] for i in agents_x_tasks if i[1] == task]) == 1

    # Restricciones auxiliares debido la reduccion de valores absolutos de la desviacion standar
    for agent in agents:
        prob += promedio_porcentaje_uso_tiempo_agentes_exepto_agente[agent] <= aux_vars[(agent, 'temporal')]
        prob += promedio_porcentaje_uso_tiempo_agentes_exepto_agente[agent] >= - aux_vars[(agent, 'temporal')]

    prob += promedio_porcentaje >= pulp.lpSum(aux_vars)
    prob += promedio_porcentaje <= pulp.lpSum(aux_vars)

    prob += promedio_porcentaje >= knowing_minimum
    prob += promedio_porcentaje <= knowing_maximum

    tiempo_solve_inicial = time()
    prob.solve(pulp.PULP_CBC_CMD(maxSeconds=maxtime))
    tiempo_final_solve = time()
    prob.writeLP("EquilibrioConHabilidades.lp")

    tiempo_solve = tiempo_final_solve - tiempo_solve_inicial

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    for v in prob.variables():
        print(re.findall(r'\d+', v.name))
        print(v.name, "=", v.varValue)
    print('El tiempo total de el solve fue:', tiempo_solve)  # En segundos
    return prob.status, prob.variables()


def solveTaskGroupingAssignment(agent_capacity, task_cost, groups, assign_same_quantity_of_tasks=False):
    """Maximize the allocation so that each agent has assigned stories highly related to each other with respect to their groups.
    Args:
        agent_capacity: {id_agent: capacity}
        task_cost: {id_task: cost}
        groups: {id_group: array of task ids}
    Returns:
        (status_problem: pulp problem status,  vars: pulp variables)
    """
    print("Agent capacities", agent_capacity.values())
    agents = agent_capacity.keys()
    tasks = task_cost.keys()
    _groups = groups.keys()
    agentsxtasks = list(itertools.product(agent_capacity.keys(),
                                          task_cost.keys()))  # Lista de pares resultante de hacer producto cartesiano entre agents y tasks
    tasks_en_groups = list(itertools.chain.from_iterable(groups.values()))
    agentsxtasks_in_groups = list(itertools.product(agent_capacity.keys(),
                                                    tasks_en_groups))  # Lista de pares resultante de hacer producto cartesiano entre agents y tasks
    agentsxgroups = list(itertools.product(agent_capacity.keys(),
                                           groups.keys()))  # Lista de pares resultante de hacer producto cartesiano entre agents y tasks
    prob = pulp.LpProblem("Task grouping assignment ", pulp.LpMinimize)
    assignment_vars = pulp.LpVariable.dicts("Assignment", agentsxtasks, None, None, pulp.LpBinary)
    # Variables Auxes para ayudarse a resolver la desviacin estandard
    aux_vars = pulp.LpVariable.dicts("Aux", agentsxtasks_in_groups, None, None)
    # Funcion objetivo

    assignment_agente_in_each_group = {}  # (idagente, idgrupo): lpSum(tasks_del_grupo_idgrupo_al_agente_idagente

    # tasks asignadas al agente por grupo
    for agente in agents:
        for grupo in _groups:
            assignment_agente_in_each_group[(agente, grupo)] = pulp.lpSum(
                [assignment_vars[x] for x in agentsxtasks if x[0] == agente and x[1] in groups[grupo]])

    # Retorna la desviacion standard de las Assignmentes a un grupo determinado

    # print (assignment_agente_in_each_group[(1,0)])
    assignment_agent_in_each_group_average = {}
    for agente in agents:
        for grupo in _groups:
            assignment_agent_in_each_group_average[(agente, grupo)] = pulp.lpSum(
                assignment_agente_in_each_group[(agente, grupo)]) / float(len(groups[grupo]))
    assigned_tasks_to_agent_less_group_average = {}
    for agente in agents:
        for grupo in _groups:
            for task in groups[grupo]:
                assigned_tasks_to_agent_less_group_average[(agente, task)] = assignment_vars[(agente, task)] - \
                                                                             assignment_agent_in_each_group_average[
                                                                                 (agente, grupo)]

    def construir_desviacion_standard(agente, grupo):
        return pulp.lpSum([aux_vars[(agente, task)] for task in groups[grupo]]) / float((len(groups[grupo])))

    def construir_funcion_objetivo():
        return pulp.lpSum(
            [construir_desviacion_standard(agentexgrupo[0], agentexgrupo[1]) for agentexgrupo in agentsxgroups])

    # Restricciones
    assignments_by_agent = {}

    for agente in agents:
        assignments_by_agent[agente] = [task_cost[i[1]] * assignment_vars[i] for i in agentsxtasks if i[0] == agente]

    # La suma de las horas asignadas no puede superar el mximo de horas disponibles
    for agente in agents:
        prob += lpSum(assignments_by_agent[agente]) <= agent_capacity[agente]
    prob += construir_funcion_objetivo(), "Minimizar desviacion estandard en la asignaciin de groups"
    # Correspondencia valores absulutos y sus respectivas variables auxiliares
    for agente in agents:
        for task in tasks_en_groups:
            prob += assigned_tasks_to_agent_less_group_average[(agente, task)] <= aux_vars[(agente, task)]
            prob += -assigned_tasks_to_agent_less_group_average[(agente, task)] <= aux_vars[(agente, task)]

    # Una task solamente puede ser asignada a una persona:

    for task in tasks:
        prob += pulp.lpSum([assignment_vars[i] for i in agentsxtasks if i[1] == task]) == 1

    tiempo_solve_inicial = time()
    prob.solve()
    tiempo_final_solve = time()
    tiempo_solve = tiempo_final_solve - tiempo_solve_inicial

    # The status of the solution is printed to the screen
    print("Status:", pulp.LpStatus[prob.status])

    for v in prob.variables():
        print(re.findall(r'\d+', v.name))
        print(v.name, "=", v.varValue)
    print('El tiempo total de el solve fue:', tiempo_solve)  # En segundos
    return prob.status, prob.variables()


def makePairs(agents, reverse=False):
    """Retorna una asignacion de parejas, de tal forma sean lo mas compatibles posibles de acuerdo a sus skills, o
        lo mas incompatibles si reverse es True

    :param agents: list Agentes for make the pairs
    :param reverse: int If true, assign pairs the most distinct than is possible

    :returns: (status, list): (Estado de el solver pulp, Lista de variables pulp con sus resultados)
    """
    problem_title = "Asignacion de parejas"
    skills_ids = agents[0].skills.keys()
    print(reverse)
    objective_type = LpMinimize if reverse else LpMaximize
    prob = LpProblem(problem_title, objective_type)
    if (len(agents) < 2):
        raise ValueError("If yout want make pairs, please give me more than one agent... ")
    # Complete odd quantity of agents with little skillful agent if want maximize compatibility, with standard
    # agent otherwise
    odd_quantity_of_agents = len(agents) % 2 == 0
    if (not odd_quantity_of_agents and not reverse):
        agents.append(Agent.get_little_skillful_agent(skills_ids))
    if (not odd_quantity_of_agents and reverse):
        agents.append(Agent.get_standard_agent(agents))
    # Si la cantidad de agentes son imapres, se debe crear un agente con id -1 cuyos atributos no
    # interfieran con la asignacion y adicionarlo a agents
    agents_ids = [agent.id for agent in agents]
    agents_dict = {agent.id: agent for agent in agents}
    print(agents_ids)
    agent_pairs = list(itertools.combinations(agents_ids, 2))
    print(agent_pairs)

    pairs_assignment = LpVariable.dicts("Asignacion", agent_pairs, None, None, LpBinary)

    pair_compatibility = {}  # agent_pair: compatibility for the pair
    for agent_pair in agent_pairs:
        agent1 = agents_dict[agent_pair[0]]
        agent2 = agents_dict[agent_pair[1]]
        pair_compatibility[agent_pair] = Agent.get_compatibility(agent1, agent2)
    # Funcion objetivo
    prob += lpSum([pair_compatibility[pair_assignment] * pairs_assignment[pair_assignment] for pair_assignment in
                   pairs_assignment])

    # Restricciones

    # Cada persona solo puede pertenecer a una pareja
    for agent_id in agents_ids:
        prob += lpSum([pairs_assignment[agent_pair] for agent_pair in agent_pairs if
                       agent_pair[0] == agent_id or agent_pair[1] == agent_id]) == 1

    tiempo_solve_inicial = time()
    prob.solve()
    tiempo_final_solve = time()

    tiempo_solve = tiempo_final_solve - tiempo_solve_inicial

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    for v in prob.variables():
        print(v.name, "=", v.varValue)
    print('El tiempo total de el solve fue:', tiempo_solve)  # En segundos
    return prob.status, prob.variables()


def assignToPairs(pairs, tasks, assign_same_quantity_of_tasks=False):
    """
    Assign tasks to pairs, by multiple characteristic punctuation
    :param pairs: dict Keys are the pair id and values are `Pair` instances, first and second
        values of the values of pairs should be are`Agent` instances
    :param tasks: list of Task
    :param assign_same_quantity_of_tasks: bool Try to assign same quantity of tasks to pairs
    :return: (pulp.Status, pulp.Variables)
    """
    pair__agents = list()
    for pair in pairs.keys():
        pair__agents.append(Agent.get_standard_agent(list(pairs[pair]), pair))
    environment = Environment(pair__agents, tasks)
    return solveAttributesAssignmentProblem(environment, assign_same_quantity_of_tasks)


def iterate_over_assignment(assignment_funct, max_iterations=12, **args):
    """
    Assign of iterative form
    :param args:
    :param assignment_funct:
    :return:
    """
    args['knowing_minimum'] = 0
    args['knowing_maximum'] = sys.maxsize
    args['maxtime'] = 16 # in secs
    vars = None
    prob_status = pulp.LpStatusNotSolved
    iterations = 0
    while pulp.LpStatusOptimal != prob_status and pulp.LpStatusInfeasible != prob_status and iterations <= max_iterations:
        prob_status, vars = assignment_funct(**args)
        iterations+=1
    return prob_status, vars
