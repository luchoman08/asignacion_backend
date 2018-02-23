from asignacionHistorias import models
from enum import Enum
import statistics as stats
class TipoAsignacion(Enum):
    """
    Contiene los tipos genericos de asignacion de historias que se puede elegir
    Atributes: 
        sencilla    asignacion con solo un valor que pondera una historias,
            la asignacion se hara manteniendo un equilibrio en los puntos asignados,
            se asume que todos los desarrolladores tienen la misma experiencia
        media   asignacion que asigna sin tener en cuenta equilibrio de puntos asignados
        compleja    asignacion basada en caracteristicas de desarrollador y de historias
    """
    sencilla = 0
    media = 1
    compleja = 2
class ModeloAsignaciones:
    """
    Contiene todo lo que una asignacion de historias de usuario en un pryecto 
    deberia tener para dar una respuesta optima
    
    Atributes:
        desarrolladores     lista de desarrolladores de el proyecto,  con
            puntuaciones especificas
        historias           lista de historias a asignar, con puntuaciones especificas
        tipoAsignacion  asignacion.TipoAsignacion
    """
    desarrolladores = []
    historias = []
    tipoAsignacion = TipoAsignacion.sencilla
    totalPuntos = None
    promedioPuntos = None
    cantidadHistorias = None
    cantidadDesarrolladores = None
    
    def getPuntuacionesGenerales(self):
        return [x.puntuacionGeneral for x in self.historias]
    
    def getDesvEstPuntosGeneralesHistorias(self):
        puntuaciones = self.getPuntuacionesGenerales()
        return stats.pstdev(puntuaciones)
        
    def getMediaPuntosGeneralesHistorias(self):
        puntuaciones = self.getPuntuacionesGenerales()
        return stats.mean(puntuaciones)
        
    def iniciarTotalPuntos(self):
        totalPuntos = 0
        for historia in self.historias:
            totalPuntos += historia.puntuacionGeneral
        self.totalPuntos = totalPuntos
    
    def iniciarPromedioPuntos(self):
        if (self.totalPuntos == None):
            self.iniciarTotalPuntos()
            self.promedioPuntos = self.totalPuntos / len(self.historias)
        else:
            self.promedioPuntos = self.totalPuntos / len(self.historias)
    
    def __init__(self, newDesarrolladores, newHistorias, newTipoAsignacion):
        self.desarrolladores = newDesarrolladores
        self.historias = newHistorias
        self.tipo_asignacion = newTipoAsignacion
        self.iniciarTotalPuntos()
        self.iniciarPromedioPuntos()
        self.cantidadDesarrolladores = len(self.desarrolladores)
        self.cantidadHistorias = len (self.historias)
        
        
    