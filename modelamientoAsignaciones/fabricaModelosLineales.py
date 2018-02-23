from asignacionHistorias import models
from . import asignacion as asig
import numpy 
import pulp
from pulp import *

def construirModeloLineal(asignacion):
    """
    Construir un modelo de programacion lineal basado en el tipo de asignacion.
    Keyword arguments:
    asignacion -- Asignacion dada, asignacion.Asignacion
    """
    if (asignacion.tipo == asig.TipoAsignacion.sencilla):
        return 0

class FabricaModeloEquilibrado:
    """
    Fabrica de modelos donde solo se tienen en cuenta las horas
    a la semana disponibles por cada desarrollador, los puntos de las historias
    y la corresondencia entre puntos de historia y horas de trabaj
    """
    asignacion = None
    nombre_desarrolladores = None
    prob = LpProblem("Problema asignacion equilibrada minimos datos", LpMinimize)
    def __init__(self, newAsignacion):
        self.asignacion = newAsignacion
    
    def initNombreDesarrolladores(self):
        self.nombre_desarrolladores = [x.nombre for x in self.asignacion.desarrolladores]
        return self.nombre_desarrolladores
    def construirFuncionObjetivo(self):
        return 0
    def construirRestriccionesNoSobrecarga(self):
        return 1
    

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
                