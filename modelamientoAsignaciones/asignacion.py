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
        desarrolladores: dict  de desarrolladores de el proyecto,  con
            horas disponibles para el sprint {'desarrolladorx': horas_disponibles}
        historias: dict de historias a asignar, con puntuaciones especificas {'historiax': puntos}
        relacion_puntos_horas: cantidad de horas estimadas que una historia tarda por cada punto 
        tipoAsignacion:  asignacion.TipoAsignacion
    """
    

    
    def __init__(self, desarrolladores, historias, relacion_puntos_horas, tipo_asignacion):
        self.desarrolladores = desarrolladores
        self.historias = historias
        self.tipo_asignacion = tipo_asignacion
        self.relacion_puntos_horas = relacion_puntos_horas
        self.cantidadDesarrolladores = len(self.desarrolladores)
        self.cantidadHistorias = len (self.historias)
        
        
    