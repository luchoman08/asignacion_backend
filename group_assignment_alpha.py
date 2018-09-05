import itertools, string, re
from pulp import *
from time import time
import math
agente_horas = {}
agente_horas[0] = 10
agente_horas[1] = 10
M = 30000000000
tarea_costo = {}
tarea_costo[0] = 5
tarea_costo[1] = 2
tarea_costo[2] = 2
tarea_costo[3] = 5
grupos = {}
grupos[0]=[0,3]
grupos[1]=[2,1]
def resolverProblemaEquilibrio(agente_horas, tarea_costo, grupos, assign_same_quantity_of_tasks = False ):
    agentes = agente_horas.keys()
    tareas = tarea_costo.keys()
    _grupos = grupos.keys()
    agentesxtareas = list(itertools.product(agente_horas.keys(), tarea_costo.keys())) # Lista de pares resultante de hacer producto cartesiano entre agentes y tareas 
    tareas_en_grupos = list(itertools.chain.from_iterable(grupos.values()))
    agentesxtareas_en_grupos = list(itertools.product(agente_horas.keys(), tareas_en_grupos)) # Lista de pares resultante de hacer producto cartesiano entre agentes y tareas 
    agentesxgrupos = list(itertools.product(agente_horas.keys(), grupos.keys())) # Lista de pares resultante de hacer producto cartesiano entre agentes y tareas 
    prob = pulp.LpProblem("Asignaciones por agrupamiento", pulp.LpMinimize) 
    variables_asignacion = pulp.LpVariable.dicts("Asignacion",agentesxtareas,None,None,pulp.LpBinary)
    #Variables auxiliares para ayudarse a resolver la desviacin estandard
    aux_vars = pulp.LpVariable.dicts("Auxiliar",  agentesxtareas_en_grupos, None, None)
    #Funcion objetivo
    

    
    asignacion_agente_en_cada_grupo = {} # (idagente, idgrupo): lpSum(tareas_del_grupo_idgrupo_al_agente_idagente

    # Tareas asignadas al agente por grupo
    for agente in agentes:
		for grupo in _grupos:
			asignacion_agente_en_cada_grupo[(agente, grupo)] = pulp.lpSum([variables_asignacion[x] for x in agentesxtareas if x[0] == agente and x[1] in grupos[grupo]  ])
	
	# Retorna la desviacion standard de las asignaciones a un grupo determinado

    #print (asignacion_agente_en_cada_grupo[(1,0)])
    promedio_asignacion_agente_en_cada_grupo = {}		
    for agente in agentes:
        for grupo in _grupos:
                promedio_asignacion_agente_en_cada_grupo[(agente, grupo)] = pulp.lpSum(asignacion_agente_en_cada_grupo[(agente, grupo)]) / float(len (grupos[grupo]))
    asignacion_historia_a_agente_menos_promedio_grupo = {}
    for agente in agentes:
		for grupo in _grupos:
		    for tarea in grupos[grupo]:
		        asignacion_historia_a_agente_menos_promedio_grupo[(agente, tarea)] = variables_asignacion[(agente, tarea)] - promedio_asignacion_agente_en_cada_grupo[(agente, grupo)]
    def construir_desviacion_standard(agente, grupo):
		return pulp.lpSum([aux_vars[(agente,tarea)] for tarea in grupos[grupo]]) / (len (grupos[grupo]) -1.0)
	    
    def construir_funcion_objetivo():
        return pulp.lpSum([construir_desviacion_standard(agentexgrupo[0], agentexgrupo[1]) for agentexgrupo in agentesxgrupos])
    #Restricciones
    cargas_por_agente = {}


    for agente in agentes:
    	cargas_por_agente[agente] = [tarea_costo [i[1]] * variables_asignacion[i] for i in agentesxtareas if i[0] == agente]

    #La suma de las horas asignadas no puede superar el mximo de horas disponibles
    for agente in agentes:
    	prob +=  lpSum(cargas_por_agente[agente]) <= agente_horas[agente]    
    prob += construir_funcion_objetivo(), "Minimizar desviacion estandard en la asignaciin de grupos"		    
    #correspondencia valores absulutos y sus respectivas variables auxiliares desvesat v1
    for agente in agentes:
		for tarea in tareas_en_grupos:
			prob+= asignacion_historia_a_agente_menos_promedio_grupo[(agente, tarea)]   <= aux_vars[(agente,tarea)]
			prob+= -asignacion_historia_a_agente_menos_promedio_grupo[(agente, tarea)] <= aux_vars[(agente,tarea)]

    #Una tarea solamente puede ser asignada a una persona:
    
    for tarea in tareas:
    	prob+= pulp.lpSum([variables_asignacion[i] for i in agentesxtareas if i[1] == tarea]) == 1
    	
    
    #for agente in agentes:
    #    prob += promedio_porcentaje_uso_tiempo_agentes_exepto_agente[agente] <= aux_vars[(agente, 'temporal')]
    #    prob += promedio_porcentaje_uso_tiempo_agentes_exepto_agente[agente] >= - aux_vars[(agente, 'temporal')]
    

    prob.writeLP("EquilibrioTrabajo.lp")
    
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
resolverProblemaEquilibrio(agente_horas, tarea_costo, grupos, True)
