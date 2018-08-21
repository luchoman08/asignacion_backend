import itertools, string, re
from pulp import *
from time import time
agente_horas = {}
agente_horas[0] = 4
agente_horas[1] = 4
agente_horas[3] = 4
M = 30000000000000000
tarea_costo = {}
tarea_costo[0] = 2
tarea_costo[1] = 1
tarea_costo[2] = 1
tarea_costo[3] = 1
grupos = {}
grupos[0]=[0,1]
grupos[1]=[2,3]
def resolverProblemaEquilibrio(agente_horas, tarea_costo, grupos ):
    agentes = agente_horas.keys()
    tareas = tarea_costo.keys()
    _grupos = grupos.keys()
    tareasxagente = list(itertools.product(agente_horas.keys(), tarea_costo.keys())) # Lista de pares resultante de hacer producto cartesiano entre agentes y tareas 
    agentesxgrupos = list(itertools.product(agente_horas.keys(), grupos.keys())) # Lista de pares resultante de hacer producto cartesiano entre agentes y tareas 
    prob = pulp.LpProblem("Asignaciones por agrupamiento", pulp.LpMaximize) 
    variables_asignacion = pulp.LpVariable.dicts("Asignacion",tareasxagente,None,None,pulp.LpBinary)
    #Variables auxiliares para ayudarse a resolver la desviacin estandard
    aux_vars = pulp.LpVariable.dicts("Auxiliar", [agentexgrupo for agentexgrupo in agentesxgrupos], None, None)
    aux_vars_bin = pulp.LpVariable.dicts("BinAux", [agentexgrupo for agentexgrupo in agentesxgrupos], None, None, pulp.LpBinary)
    #Funcion objetivo
    
    def construir_desviacion_standard_vars(grupo):
		return pulp.lpSum([aux_vars[(agente,grupo)] for agente in agentes]) / (float(len(agentes)) -1)
    
    def construir_funcion_objetivo():
        return pulp.lpSum([construir_desviacion_standard_vars(grupo) for grupo in _grupos])
    
    
    prob += construir_funcion_objetivo(), "Minimizar desviacion estandard en la asignacin de grupos"
    
    asignacion_agente_en_cada_grupo = {} # (idagente, idgrupo): lpSum(tareas_del_grupo_idgrupo_al_agente_idagente
    cargas_por_agente = {}
    
    
    for agente in agentes:
    	cargas_por_agente[agente] = [tarea_costo [i[1]] * variables_asignacion[i] for i in tareasxagente if i[0] == agente]
     
    # Tareas asignadas al agente por grupo
    for agente in agentes:
		for grupo in _grupos:
			asignacion_agente_en_cada_grupo[(agente, grupo)] = pulp.lpSum([variables_asignacion[x] for x in tareasxagente if x[0] == agente and x[1] in grupos[grupo]  ])
	
	# Retorna la desviacion standard de las asignaciones a un grupo determinado

    #print (asignacion_agente_en_cada_grupo[(1,0)])
    promedio_cantidad_historias_asignadas_por_grupo = {} # idgrupo: promedio_asignaciones_a_los_Agentes_en_cada_grupo, promedio_asignaciones_a_los_Agentes_en_cada_grupo = sumatoria(asignaciones_grupo_a_cada_agente)/num_agentes
    for grupo in _grupos:
		promedio_cantidad_historias_asignadas_por_grupo[grupo] = pulp.lpSum([asignacion_agente_en_cada_grupo[(agente, grupo)] for agente in agentes]) / float(len(agentes))
	#esto es lo que va en el valor absoluto	
    def asignacion_grupo_a_agente_menos_promedio_grupo(agente, grupo):
		return asignacion_agente_en_cada_grupo[(agente, grupo)] - promedio_cantidad_historias_asignadas_por_grupo[grupo]		
    
    
    #correspondencia valores absulutos y sus respectivas variables auxiliares
    for agente in agentes:
		for grupo in grupos:
			prob+= (asignacion_grupo_a_agente_menos_promedio_grupo(agente, grupo) + M * aux_vars_bin[(agente, grupo)])  >= aux_vars[(agente,grupo)]
			prob+= (-asignacion_grupo_a_agente_menos_promedio_grupo(agente, grupo) + M * (1 - aux_vars_bin[(agente, grupo)] ))  >= aux_vars[(agente,grupo)]
			prob+= asignacion_grupo_a_agente_menos_promedio_grupo(agente, grupo)   <= aux_vars[(agente,grupo)]
			prob+= -asignacion_grupo_a_agente_menos_promedio_grupo(agente, grupo) <= aux_vars[(agente,grupo)]
    #La suma de las horas asignadas no puede superar el mximo de horas disponibles
    for agente in agentes:
    	prob +=  pulp.lpSum(cargas_por_agente[agente]) <= agente_horas[agente]
        
    #Una tarea solamente puede ser asignada a una persona:
    
    for tarea in tareas:
    	prob+= pulp.lpSum([variables_asignacion[i] for i in tareasxagente if i[1] == tarea]) == 1
    	
    
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
resolverProblemaEquilibrio(agente_horas, tarea_costo, grupos)
