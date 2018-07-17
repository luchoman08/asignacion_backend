import itertools, string, re
from pulp import *
from time import time
import math
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
tarea = Task (1, costo_caracteristica)
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
agente = Agent (1, habilidad_caracteristica)
agente_ = Agent (2, habilidad_caracteristica_)


class Environment:

    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks
        self.costos = {}
        self.agentes_dict = {agente.id: agente for agente in agents}
        self.tareas_dict = {tarea.id: tarea for tarea in tasks}
        self.agentesxtareas = list(itertools.product(self.agentes_dict.keys(), self.tareas_dict.keys()))
        self.init_costos()

    def init_costos(self):
        for agentextarea in self.agentesxtareas:
            self.costos[agentextarea] = self.calcular_costo(self.agentes_dict[agentextarea[0]], self.tareas_dict[agentextarea[1]])

    def calcular_costo(self, agente, tarea):
        costo = 0
        for id_caracteristica in tarea.costo_caracteristica.keys():
            costo += tarea.costo_caracteristica[id_caracteristica] * tarea.costo_caracteristica[id_caracteristica] / agente.habilidad_caracteristica[id_caracteristica]
        return costo

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
        self.agentes_dict = {agente.id: agente for agente in agents}
        self.tareas_dict = {tarea.id: tarea for tarea in tasks}
        self.relaciones_tareas_dict  = {grupo_tarea['id_externo']: grupo_tarea['id_historias'] for grupo_tarea in self.grupo_tareas }
        self.agentesxtareas = list(itertools.product(self.agentes_dict.keys(), self.tareas_dict.keys()))
        self.agentesxrelaciones_tareas = list(itertools.product(self.agentes_dict.keys(), self.relaciones_tareas_dict.keys()))
        self.init_costos()
        self.init_costos_grupo()


    def calcular_costo(self, agente, tarea):
        costo = 0
        for id_caracteristica in tarea.costo_caracteristica.keys():
            costo += tarea.costo_caracteristica[id_caracteristica] * tarea.costo_caracteristica[id_caracteristica] / agente.habilidad_caracteristica[id_caracteristica]
        return costo
    def costoGrupoTareas(self, id_tareas, agente):
        resultado = 0
        for id_tarea in id_tareas:
            resultado += self.calcular_costo(agente, self.tareas_dict[id_tarea])
        return resultado

    def init_costos(self):
        for agentextarea in self.agentesxtareas:
            self.costos[agentextarea] = self.calcular_costo(self.agentes_dict[agentextarea[0]], self.tareas_dict[agentextarea[1]])

    def init_costos_grupo(self):
        for agentexrelacion_tareas in self.agentesxrelaciones_tareas:
            self.costos_grupo[agentexrelacion_tareas] = self.costoGrupoTareas(self.relaciones_tareas_dict[agentexrelacion_tareas[1]], self.agentes_dict[agentexrelacion_tareas[0]])




agents = [agente, agente_]
tasks = [tarea, tarea_]
entorno = Environment(agents, tasks)

def solveAttributesAssignmentProblem(entorno, procurar_misma_cantidad_tareas=False):
    """Resuelve el problema de la asignacion garantizando un equilibrio en las cargas asignadas, adicionando
    puntuacion de el agente en caracteristicas especificas y costos en las tasks .

    La escala de habilidades_caracteristica es del 0 al 10
    La escala de costo_caracteristica es del 0 al 10
    Se asignan las tasks de tal forma que se minimize la diferencia de cargas asignadas, en
    porcentaje con respecto al costo basado en que tanto le cuesta a cada agente hacer sus asignaciones,
    dependiendo sus habilidades y el costo definido en distintos argumentos de la tarea

    Args:
        agents (list of ´´Agente´´): Agentes a asignar
        tasks (list of ´´Tarea´´): Tareas a asignar
    Returns:
        (status, list): (Estado de el solver pulp, Lista de variables pulp con sus resultados)


    """
    print(entorno.agents[1].id, " ", entorno.agents[1].habilidad_caracteristica)
    prob = LpProblem("Equilibrio de asignaciones", LpMinimize)
    variables_asignacion = LpVariable.dicts("Asignacion",entorno.agentesxtareas,None,None,LpBinary)

    #Funcion objetivo

    prob += lpSum([entorno.costos[agentextarea] * variables_asignacion[agentextarea] for agentextarea in entorno.agentesxtareas])
    #Una tarea solamente puede ser asignada a una persona:

    for tarea in entorno.tasks:
    	prob += lpSum([variables_asignacion[agentextarea] for agentextarea in entorno.agentesxtareas if agentextarea[1] == tarea.id]) == 1

    if procurar_misma_cantidad_tareas:

        minimas_tareas = math.floor(len(entorno.tasks) / len(entorno.agents) )
        for agente in entorno.agents:
            prob += lpSum([variables_asignacion[agentextarea] for agentextarea in entorno.agentesxtareas if agentextarea[0] == agente.id]) >= minimas_tareas

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

solveAttributesAssignmentProblem(entorno, procurar_misma_cantidad_tareas=True)















def solveEquilibriumProblem(agente_capacidad, tarea_costo):
    print(agente_capacidad)
    print(tarea_costo)
    """Resuelve el problema de la asignación garantizando un equilibrio en las cargas asignadas.

    Se asignan las tasks de tal forma que se minimize la diferencia de cargas asignadas, en
    porcentaje con respecto a la capacidad disponibles por cada agente

    Args:
        agente_capacidad (dict of str: int): Identificacion de el agente como llave, la capacidad es el valor.
        tarea_costo (dict of str: int): Identificacion de la tarea como llave, su costo es el valor.

    Returns:
        (status, list): (Estado de el solver pulp, Lista de variables pulp con sus resultados)


    """
    agents = agente_capacidad.keys()
    tasks = tarea_costo.keys()
    agentesxtareas = list(itertools.product(agente_capacidad.keys(), tarea_costo.keys())) # Lista de pares resultante de hacer producto cartesiano entre agents y tasks
    prob = LpProblem("Equilibrio de asignaciones", LpMinimize)
    variables_asignacion = LpVariable.dicts("Asignacion",agentesxtareas,None,None,LpBinary)
    #Variables auxiliares para ayudarse a resolver la desviacin estandard
    aux_vars = LpVariable.dicts("Auxiliar", [(a, "temporal") for a in agents], None, None)
    #Funcion objetivo



    def construir_funcion_objetivo(agents):
        return lpSum(aux_vars)


    prob += construir_funcion_objetivo(agents), "Minimizar desviacion estandard de el trabajo"

    porcentaje_uso_tiempo_agentes = {}
    cargas_por_agente = {}


    for agente in agents:
    	cargas_por_agente[agente] = [tarea_costo [i[1]] * variables_asignacion[i] for i in agentesxtareas if i[0] == agente]


    for agente in agents:
    	porcentaje_uso_tiempo_agentes[agente] = lpSum([x * 100 / agente_capacidad[agente] for x in cargas_por_agente[agente] ])

    promedio_porcentaje_uso_tiempo_agentes_exepto_agente = {}

    porcentaje_uso_tiempo_agentes_menos_porcentaje_uso_tiempo_agente_dividido_longitud_agentes = {}
    for agente in agents:
    	porcentaje_uso_tiempo_agentes_menos_porcentaje_uso_tiempo_agente_dividido_longitud_agentes[agente] =	porcentaje_uso_tiempo_agentes[agente] - porcentaje_uso_tiempo_agentes[agente]  / len(agents)

    for agente in agents:
    	promedio_porcentaje_uso_tiempo_agentes_exepto_agente[agente] = \
    	(-lpSum([porcentaje_uso_tiempo_agentes[agentex] \
    	for agentex in agents if agentex != agente]) /  len(agents)) + porcentaje_uso_tiempo_agentes_menos_porcentaje_uso_tiempo_agente_dividido_longitud_agentes[agente]


    #Restricciones

    #La suma de las horas asignadas no puede superar el mximo de horas disponibles
    for agente in agents:
    	prob +=  lpSum(cargas_por_agente[agente]) <= agente_capacidad[agente]

    #Una tarea solamente puede ser asignada a una persona:

    for tarea in tasks:
    	prob+= lpSum([variables_asignacion[i] for i in agentesxtareas if i[1] == tarea]) == 1

    # Restricciones auxiliares debido la reduccion de valores absolutos de la desviacion standar
    for agente in agents:
        prob += promedio_porcentaje_uso_tiempo_agentes_exepto_agente[agente] <= aux_vars[(agente, 'temporal')]
        prob += promedio_porcentaje_uso_tiempo_agentes_exepto_agente[agente] >= - aux_vars[(agente, 'temporal')]
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

