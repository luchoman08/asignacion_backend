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

class FabricaModeloLinealUnicaPonderacion:
    asignacion = None
    def __init__(self, newAsignacion):
        self.asignacion = newAsignacion    
        
    def construirModeloLinealUnicaPonderacion(self):
        """
        Construir un modelo de programacion lineal basado en el tipo de asignacion.
        Keyword arguments:
        asignacion -- Asignacion dada, asignacion.Asignacion
        """
    
    def construirTotalRestricciones(self):
        restriccionesEquilibrio, vectorTopeEquilibrio = self.restriccionesEquilibrioAsignacion()
        restriccionesCumplirCadaHistoria, vectorTopeCumplirCada = self.restriccionesCumplirTodasHistorias()
        vectorTopeBool = self.restriccionesVariablesBooleanas()
        vectorTope = []
        vectorTope.append(vectorTopeEquilibrio,vectorTopeCumplirCada,vectorTopeBool)
        
        
        
    def cantidadVariablesDesicion(self):
        return self.asignacion.cantidadHistorias * self.asignacion.cantidadDesarrolladores
        
    def restriccionesEquilibrioAsignacion(self):
        topeMaximo = self.asignacion.getMediaPuntosGeneralesHistorias() + self.asignacion.getDesvEstPuntosGeneralesHistorias()
        vectorTope = [topeMaximo for i in range(0, self.asignacion.cantidadDesarrolladores  )]
        restricciones = [[1 for x in range (0, self.cantidadVariablesDesicion() )] for j in range (0,self.asignacion.cantidadDesarrolladores)]
        return restricciones, vectorTope

    def funcionMaximizar(self):
        return [1 for x in range(self.cantidadVariablesDesicion() )]
    
    def restriccionesCumplirTodasHistorias(self):
        restricciones = numpy.zeros((  self.asignacion.cantidadHistorias*2, self.cantidadVariablesDesicion() ))
        topePositivo = [1 for i in range(0, self.asignacion.cantidadHistorias )]
        topeNegativo = [-1 for i in range(0, self.asignacion.cantidadHistorias  )]
        
        for x in range (0 , self.asignacion.cantidadDesarrolladores):
            for i in range (0, self.cantidadVariablesDesicion(), self.asignacion.cantidadHistorias):
                print(restricciones)
                print('\n')
                restricciones[x][i:self.asignacion.cantidadDesarrolladores] = [1 for x in range(0, self.asignacion.cantidadDesarrolladores)]
                
        for x in range (self.asignacion.cantidadHistorias - 1, (self.asignacion.cantidadHistorias * 2) -1):
            for i in range (0, self.cantidadVariablesDesicion() , self.asignacion.cantidadDesarrolladores):
                restricciones[x][i:self.asignacion.cantidadDesarrolladores] = [-1 for x in range(0, self.asignacion.cantidadDesarrolladores)]
        return restricciones, topePositivo.extend(topeNegativo)
    
    def restriccionesVariablesBooleanas(self):
        return [(1,1) for x in range(0, self.cantidadVariablesDesicion())]
                
