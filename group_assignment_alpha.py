import itertools, string, re
from pulp import *
from time import time
import math
agent_capacity = {}
agent_capacity[0] = 10
agent_capacity[1] = 10
task_cost = {}
task_cost[0] = 5
task_cost[1] = 2
task_cost[2] = 2
task_cost[3] = 5
groups = {}
groups[0]=[0,3]
groups[1]=[2,1]
def solveTaskGroupingAssignment(agent_capacity, task_cost, groups, assign_same_quantity_of_tasks = False ):
    """Maximize the allocation so that each agent has assigned stories highly related to each other with respect to their groups.
    Args:
        agent_capacity: {id_agent: capacity}
        task_cost: {id_task: cost}
        groups: {id_group: array of task ids}
    Returns:
        (status_problem: pulp problem status,  vars: pulp variables)
    """
    agents = agent_capacity.keys()
    tasks = task_cost.keys()
    _groups = groups.keys()
    agentsxtasks = list(itertools.product(agent_capacity.keys(), task_cost.keys())) # Lista de pares resultante de hacer producto cartesiano entre agents y tasks 
    tasks_en_groups = list(itertools.chain.from_iterable(groups.values()))
    agentsxtasks_in_groups = list(itertools.product(agent_capacity.keys(), tasks_en_groups)) # Lista de pares resultante de hacer producto cartesiano entre agents y tasks 
    agentsxgroups = list(itertools.product(agent_capacity.keys(), groups.keys())) # Lista de pares resultante de hacer producto cartesiano entre agents y tasks 
    prob = pulp.LpProblem("Task grouping assignment ", pulp.LpMinimize) 
    assignment_vars = pulp.LpVariable.dicts("Assignment",agentsxtasks,None,None,pulp.LpBinary)
    #Variables Auxes para ayudarse a resolver la desviacin estandard
    aux_vars = pulp.LpVariable.dicts("Aux",  agentsxtasks_in_groups, None, None)
    #Funcion objetivo
    
    assignment_agente_in_each_group = {} # (idagente, idgrupo): lpSum(tasks_del_grupo_idgrupo_al_agente_idagente

    # tasks asignadas al agente por grupo
    for agente in agents:
		for grupo in _groups:
			assignment_agente_in_each_group[(agente, grupo)] = pulp.lpSum([assignment_vars[x] for x in agentsxtasks if x[0] == agente and x[1] in groups[grupo]  ])
	
	# Retorna la desviacion standard de las Assignmentes a un grupo determinado

    #print (assignment_agente_in_each_group[(1,0)])
    assignment_agent_in_each_group_average = {}		
    for agente in agents:
        for grupo in _groups:
                assignment_agent_in_each_group_average[(agente, grupo)] = pulp.lpSum(assignment_agente_in_each_group[(agente, grupo)]) / float(len (groups[grupo]))
    assigned_tasks_to_agent_less_group_average = {}
    for agente in agents:
		for grupo in _groups:
		    for task in groups[grupo]:
		        assigned_tasks_to_agent_less_group_average[(agente, task)] = assignment_vars[(agente, task)] - assignment_agent_in_each_group_average[(agente, grupo)]
    def construir_desviacion_standard(agente, grupo):
		return pulp.lpSum([aux_vars[(agente,task)] for task in groups[grupo]]) / (len (groups[grupo]) -1.0)
	    
    def construir_funcion_objetivo():
        return pulp.lpSum([construir_desviacion_standard(agentexgrupo[0], agentexgrupo[1]) for agentexgrupo in agentsxgroups])
    #Restricciones
    assignments_by_agent = {}


    for agente in agents:
    	assignments_by_agent[agente] = [task_cost [i[1]] * assignment_vars[i] for i in agentsxtasks if i[0] == agente]

    #La suma de las horas asignadas no puede superar el mximo de horas disponibles
    for agente in agents:
    	prob +=  lpSum(assignments_by_agent[agente]) <= agent_capacity[agente]    
    prob += construir_funcion_objetivo(), "Minimizar desviacion estandard en la asignaciin de groups"		    
    # Correspondencia valores absulutos y sus respectivas variables auxiliares
    for agente in agents:
		for task in tasks_en_groups:
			prob+= assigned_tasks_to_agent_less_group_average[(agente, task)]   <= aux_vars[(agente,task)]
			prob+= -assigned_tasks_to_agent_less_group_average[(agente, task)] <= aux_vars[(agente,task)]

    #Una task solamente puede ser asignada a una persona:
    
    for task in tasks:
    	prob+= pulp.lpSum([assignment_vars[i] for i in agentsxtasks if i[1] == task]) == 1
    	
    
    tiempo_solve_inicial = time() 
    prob.solve()
    tiempo_final_solve = time() 
    tiempo_solve = tiempo_final_solve - tiempo_solve_inicial
    
    # The status of the solution is printed to the screen
    print("Status:", pulp.LpStatus[prob.status])
    
    for v in prob.variables():
        print(re.findall(r'\d+', v.name))
        print(v.name, "=", v.varValue)
    
    
    print ('El tiempo total de el solve fue:', tiempo_solve) #En segundos 
solveTaskGroupingAssignment(agent_capacity, task_cost, groups, True)
