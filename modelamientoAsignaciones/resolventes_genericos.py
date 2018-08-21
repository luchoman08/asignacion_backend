import itertools, string, re
from pulp import *
from time import time
import math
import numbers

class Task:

    def __init__(self, id, costo_caracteristica ):
        self.id = id
        self.costo_caracteristica = costo_caracteristica #dict

costo_caracteristica = {}
costo_caracteristica[1] = 0
costo_caracteristica[2] = 10
costo_caracteristica[3] = 0
costo_caracteristica_ = {}
costo_caracteristica_[1] = 10
costo_caracteristica_[2] = 0
costo_caracteristica_[3] = 0
task = Task (1, costo_caracteristica)
tarea_ = Task (2, costo_caracteristica_)

class Agent:

    def __init__(self, id, habilidad_caracteristica ):
        self.id = id
        self.habilidad_caracteristica = habilidad_caracteristica #dict

habilidad_caracteristica = {}
habilidad_caracteristica[1] = 10
habilidad_caracteristica[2] = 1
habilidad_caracteristica[3] = 1
habilidad_caracteristica_ = {}
habilidad_caracteristica_[1] = 1
habilidad_caracteristica_[2] = 10
habilidad_caracteristica_[3] = 1
agent = Agent (1, habilidad_caracteristica)
agente_ = Agent (2, habilidad_caracteristica_)


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
            self.costos[agentextarea] = self.get_cost(self.agents_dict[agentextarea[0]], self.tasks_dict[agentextarea[1]])

    def get_cost(self, agent, task):
        cost = 0
        for id_caracteristica in task.costo_caracteristica.keys():
			# La habilidad caracteristica no puede ser 0 dado que se usa en una división, para este modelo el minimo de habilidad es 0.1, por ende para prevenir errores se normaliza esta propiedad
            habilidad_caracteristica_normalizada = agent.habilidad_caracteristica[id_caracteristica] if isinstance(agent.habilidad_caracteristica[id_caracteristica], numbers.Number) and agent.habilidad_caracteristica[id_caracteristica] != 0  else 0.1 
            cost += task.costo_caracteristica[id_caracteristica] * task.costo_caracteristica[id_caracteristica] / habilidad_caracteristica_normalizada
        return cost

class GrupoIdsHistorias:
    """
    id: string
    ids: [string]

    """
    def __init__(self, id_grupo, ids):
        self.id_grupo = id_grupo
        self.ids = ids


class EntornoConGruposHistorias:

    def __init__(self, agents, tasks, grupo_tareas, caracteristicas):
        self.agents = agents
        self.grupo_tareas = grupo_tareas
        self.tasks = tasks
        self.caracteristicas = caracteristicas #dict
        self.costos = {}
        self.costos_grupo = {}
        self.agents_dict = {agent.id: agent for agent in agents}
        self.tasks_dict = {task.id: task for task in tasks}
        self.relaciones_tareas_dict  = {grupo_tarea['id_externo']: grupo_tarea['id_historias'] for grupo_tarea in self.grupo_tareas }
        self.agents_x_tasks = list(itertools.product(self.agents_dict.keys(), self.tasks_dict.keys()))
        self.agentesxrelaciones_tareas = list(itertools.product(self.agents_dict.keys(), self.relaciones_tareas_dict.keys()))
        self.init_cost()
        self.init_costos_grupo()


    def get_cost(self, agent, task):
        cost = 0
        for id_caracteristica in task.costo_caracteristica.keys():
            cost += task.costo_caracteristica[id_caracteristica] * task.costo_caracteristica[id_caracteristica] / agent.habilidad_caracteristica[id_caracteristica]
        return cost
    def costoGrupoTareas(self, id_tareas, agent):
        resultado = 0
        for id_tarea in id_tareas:
            resultado += self.get_cost(agent, self.tasks_dict[id_tarea])
        return resultado

    def init_cost(self):
        for agentextarea in self.agents_x_tasks:
            self.costos[agentextarea] = self.get_cost(self.agents_dict[agentextarea[0]], self.tasks_dict[agentextarea[1]])

    def init_costos_grupo(self):
        for agentexrelacion_tareas in self.agentesxrelaciones_tareas:
            self.costos_grupo[agentexrelacion_tareas] = self.costoGrupoTareas(self.relaciones_tareas_dict[agentexrelacion_tareas[1]], self.agents_dict[agentexrelacion_tareas[0]])




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
    print(environment.agents[1].id, " ", environment.agents[1].habilidad_caracteristica)
    prob = LpProblem("Equilibrio de asignaciones", LpMinimize)
    variables_asignacion = LpVariable.dicts("Asignacion",environment.agents_x_tasks,None,None,LpBinary)

    #Funcion objetivo

    prob += lpSum([environment.costos[agentextarea] * variables_asignacion[agentextarea] for agentextarea in environment.agents_x_tasks])
    #Una task solamente puede ser asignada a una persona:

    for task in environment.tasks:
    	prob += lpSum([variables_asignacion[agentextarea] for agentextarea in environment.agents_x_tasks if agentextarea[1] == task.id]) == 1

    if assign_same_quantity_of_tasks:

        minimas_tareas = math.floor(len(environment.tasks) / len(environment.agents) )
        for agent in environment.agents:
            prob += lpSum([variables_asignacion[agentextarea] for agentextarea in environment.agents_x_tasks if agentextarea[0] == agent.id]) >= minimas_tareas

    prob.writeLP("EquilibrioConHabilidades.lp")
    tiempo_solve_inicial = time()
    prob.solve()
    tiempo_final_solve = time()


    tiempo_solve = tiempo_final_solve - tiempo_solve_inicial

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    for v in prob.variables():
        print(v.name, "=", v.varValue)
    print ('El tiempo total de el solve fue:', tiempo_solve) #En segundos
    return prob.status,  prob.variables()

solveAttributesAssignmentProblem(environment, assign_same_quantity_of_tasks=True)















def solveEquilibriumProblem(agente_capacidad, tarea_costo):
    print(agente_capacidad)
    print(tarea_costo)
    """Resuelve el problema de la asignación garantizando un equilibrio en las cargas asignadas.

    Se asignan las tasks de tal forma que se minimize la diferencia de cargas asignadas, en
    porcentaje con respecto a la capacidad disponibles por cada agent

    Args:
        agente_capacidad (dict of str: int): Identificacion de el agent como llave, la capacidad es el valor.
        tarea_costo (dict of str: int): Identificacion de la task como llave, su cost es el valor.

    Returns:
        (status, list): (Estado de el solver pulp, Lista de variables pulp con sus resultados)


    """
    agents = agente_capacidad.keys()
    tasks = tarea_costo.keys()
    agents_x_tasks = list(itertools.product(agente_capacidad.keys(), tarea_costo.keys())) # Lista de pares resultante de hacer producto cartesiano entre agents y tasks
    prob = LpProblem("Equilibrio de asignaciones", LpMinimize)
    variables_asignacion = LpVariable.dicts("Asignacion",agents_x_tasks,None,None,LpBinary)
    #Variables auxiliares para ayudarse a resolver la desviacin estandard
    aux_vars = LpVariable.dicts("Auxiliar", [(a, "temporal") for a in agents], None, None)
    #Funcion objetivo



    def construir_funcion_objetivo(agents):
        return lpSum(aux_vars)


    prob += construir_funcion_objetivo(agents), "Minimizar desviacion estandard de el trabajo"

    porcentaje_uso_tiempo_agentes = {}
    cargas_por_agente = {}


    for agent in agents:
    	cargas_por_agente[agent] = [tarea_costo [i[1]] * variables_asignacion[i] for i in agents_x_tasks if i[0] == agent]


    for agent in agents:
    	porcentaje_uso_tiempo_agentes[agent] = lpSum([x * 100 / agente_capacidad[agent] for x in cargas_por_agente[agent] ])

    promedio_porcentaje_uso_tiempo_agentes_exepto_agente = {}

    porcentaje_uso_tiempo_agentes_menos_porcentaje_uso_tiempo_agente_dividido_longitud_agentes = {}
    for agent in agents:
    	porcentaje_uso_tiempo_agentes_menos_porcentaje_uso_tiempo_agente_dividido_longitud_agentes[agent] =	porcentaje_uso_tiempo_agentes[agent] - porcentaje_uso_tiempo_agentes[agent]  / len(agents)

    for agent in agents:
    	promedio_porcentaje_uso_tiempo_agentes_exepto_agente[agent] = \
    	(-lpSum([porcentaje_uso_tiempo_agentes[agentex] \
    	for agentex in agents if agentex != agent]) /  len(agents)) + porcentaje_uso_tiempo_agentes_menos_porcentaje_uso_tiempo_agente_dividido_longitud_agentes[agent]


    #Restricciones

    #La suma de las horas asignadas no puede superar el mximo de horas disponibles
    for agent in agents:
    	prob +=  lpSum(cargas_por_agente[agent]) <= agente_capacidad[agent]

    #Una task solamente puede ser asignada a una persona:

    for task in tasks:
    	prob+= lpSum([variables_asignacion[i] for i in agents_x_tasks if i[1] == task]) == 1

    # Restricciones auxiliares debido la reduccion de valores absolutos de la desviacion standar
    for agent in agents:
        prob += promedio_porcentaje_uso_tiempo_agentes_exepto_agente[agent] <= aux_vars[(agent, 'temporal')]
        prob += promedio_porcentaje_uso_tiempo_agentes_exepto_agente[agent] >= - aux_vars[(agent, 'temporal')]
    #prob.writeLP("EquilibrioTrabajo.lp")

    tiempo_solve_inicial = time()
    prob.solve()
    tiempo_final_solve = time()
    prob.writeLP("EquilibrioConHabilidades.lp")

    tiempo_solve = tiempo_final_solve - tiempo_solve_inicial

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    for v in prob.variables():
        print(re.findall(r'\d+', v.name))
        print(v.name, "=", v.varValue)
    print ('El tiempo total de el solve fue:', tiempo_solve) #En segundos
    return prob.status,  prob.variables()

