from asignacionHistorias import models
from . import asignacion as asig
from . import resolventes_genericos as resol_genericos
import pulp
import re

class FabricaModeloEquilibrado:
    """
    Fabrica de modelos donde solo se tienen en cuenta las horas
    a la semana disponibles por cada desarrollador, los puntos de las historias
    y la corresondencia entre puntos de historia y horas de trabaj
    """

    def __init__(self, agentes, tareas, relacion_horas_puntos):
        self.agentes = agentes
        self.tareas = tareas
        self.relacion_horas_puntos = relacion_horas_puntos
        self.agentes_horas = {agente.id_externo: agente.horasDisponiblesSemana for agente in self.agentes }
        self.tareas_horas = {tarea.id_externo: tarea.puntuacionGeneral * self.relacion_horas_puntos for tarea in self.tareas }
    
    def solve(self):
        pulp_status, pulp_variables = resol_genericos.resolverProblemaEquilibrio(self.agentes_horas, self.tareas_horas)
        asignaciones_resultado = {int(agente):[] for agente in self.agentes_horas.keys()}
        
        for variable in pulp_variables:
            numeros_en_nombre_variable = re.findall(r'\d+', variable.name)
            if (len(numeros_en_nombre_variable) == 2 and variable.varValue == 1):
                agente = int(numeros_en_nombre_variable[0])
                tarea = int(numeros_en_nombre_variable[1])
                asignaciones_resultado[agente].append(tarea)
        print(asignaciones_resultado)
        return asignaciones_resultado

class FabricaModeloPorAtributos:
    """
    Fabrica de modelos donde se tienen en cuenta las habilidades de cada desarrollador (agente ) y
    los costos de cada historia (tarea) medidos por caracteristicas, podiendo mantener un equilibrio
    entre cantidad de historias asignadas o bien un minimo de historias asignadas a cada desarrollador
    """ 
    

    def __init__(self, agentes, tareas, caracteristicas, puntuacion_atributos_agente, puntuacion_atributos_tarea, procurar_misma_cantidad_tareas):
        self.puntuacion_atributos_tarea = puntuacion_atributos_tarea
        self.puntuacion_atributos_agente = puntuacion_atributos_agente
        puntuacion_atributos_agente_dict = self.getpuntuacion_atributos_agente_dict(agentes)
        puntuacion_atributos_tarea_dict = self.getpuntuacion_atributos_tarea_dict(tareas)
        self.agentes = [resol_genericos.Agente(agente.id_externo, puntuacion_atributos_agente_dict[agente.id_externo]) for agente in agentes]
        self.tareas = [resol_genericos.Tarea(tarea.id_externo, puntuacion_atributos_tarea_dict[tarea.id_externo]) for tarea in tareas]
        self.caracteristicas = caracteristicas
        self.procurar_misma_cantidad_tareas = procurar_misma_cantidad_tareas
        self.entorno = resol_genericos.Entorno(self.agentes, self.tareas, self.caracteristicas)
        
    def getpuntuacion_atributos_agente_dict(self, agentes):
        puntuacion_atributos_agente_dict = {agente.id_externo: {} for agente in agentes}
        for puntuacion in self.puntuacion_atributos_agente:
            puntuacion_atributos_agente_dict[puntuacion.desarrollador.id_externo][puntuacion.atributo] = puntuacion.puntuacion
        return  puntuacion_atributos_agente_dict
     
    def getpuntuacion_atributos_tarea_dict(self, tareas):
        puntuacion_atributos_tarea_dict = {tarea.id_externo: {} for tarea in tareas}
        print(puntuacion_atributos_tarea_dict.keys())
        for puntuacion in self.puntuacion_atributos_tarea:
            puntuacion_atributos_tarea_dict[puntuacion.historia.id_externo][puntuacion.atributo] = puntuacion.puntuacion
        return   puntuacion_atributos_tarea_dict
    def solve(self):
        
        pulp_status, pulp_variables = resol_genericos.resolverProblemaEquilibrioConHabilidades(self.entorno, procurar_misma_cantidad_tareas = self.procurar_misma_cantidad_tareas  )
        asignaciones_resultado = {int(agente.id):[] for agente in self.agentes}
        
        for variable in pulp_variables:
            numeros_en_nombre_variable = re.findall(r'\d+', variable.name)
            if (len(numeros_en_nombre_variable) == 2 and variable.varValue == 1):
                agente = int(numeros_en_nombre_variable[0])
                tarea = int(numeros_en_nombre_variable[1])
                asignaciones_resultado[agente].append(tarea)
        print(asignaciones_resultado)
        return asignaciones_resultado