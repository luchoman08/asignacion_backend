import itertools, string, re
from pulp import *
from time import time
import math
import numbers
from functools import reduce




class Agent:
    DEFAULT_ID = 854554
    DEFAULT_SKILL_ID = -1
    MINIMUM_SKILL_VALUE = 1
    def __init__(self, id, skills ):
        self.id = id
        self.skills = skills #dict (id_habilidad): valor_habilidad; valor_habilidad >= MINIMUM_SKILL_VALUE
        
    @staticmethod
    def get_standard_agent(agents):
        """Retorna un agente cuyas skills son la media de un grupo de agentes, debe haber almenos un agente,
        el id de este agente sera DEFAULT_ID
        Args:
            agents: list of Agent
        Returns: 
            agent: instance of Agent
        """
        
        if(len(agents)<=0):
            raise ValueError('Debe ingresar almenos un agente')
        elif(len(agents)==1):
            return  Agent(Agent.DEFAULT_ID, agents[0].skills)
        id_skills = agents[0].skills.keys()
        cantidad_agentes = len(agents)
        skills_media = {id_habilidad: Agent.DEFAULT_SKILL_ID for id_habilidad in id_skills}
        for id_habilidad in id_skills:
            skills_media[id_habilidad] = reduce((lambda x, y: x + y), [agent.skills[id_habilidad] for agent in agents]) / float(cantidad_agentes)
        return  Agent(Agent.DEFAULT_ID, skills_media)
        
    @staticmethod
    def get_little_skillful_agent(id_skills):
        """Retorna un agente con las skills mas bajas posibles
        Args:
            id_habilities: list of integer
        Return:
            little_skillful_agent: Agent
        """
        skills = {id_skill: Agent.MINIMUM_SKILL_VALUE for id_skill in id_skills}
        return Agent(Agent.DEFAULT_ID, skills)
        
    @staticmethod    
    def get_compatibility(agent1, agent2):
        """Retorna la compatibilidad del 1 al 100 la cual indica que tan compatibles son dos agentes
        Args:
            agent1: Agent
            agent2: Agent
        Returns:
            compatibility: int Compatibilidad entre los agentes, valor del 1 al 100, donde a mayor valor mayor compatibilidad
        """
        compatibility = 0
        id_skills = agent1.skills.keys()
        cantidad_skills = len(id_skills)
        porcentaje_importancia_por_habilidad = 1 / float (cantidad_skills)
        compatibility_func = lambda habilidad1, habilidad2:  min(habilidad1, habilidad2) * 100 / max(habilidad1, habilidad2) 
        for id_habilidad in id_skills:
            compatibility += porcentaje_importancia_por_habilidad * compatibility_func(agent1.skills[id_habilidad], agent2.skills[id_habilidad])
        return compatibility
skills = {}
skills[1] = 10
skills[2] = 1
skills[3] = 1
skills_ = {}
skills_[1] = 1
skills_[2] = 10
skills_[3] = 1
skills__ = {}
skills__[1] = 1
skills__[2] = 10
skills__[3] = 1
agent = Agent (1, skills)
agente_ = Agent (2, skills_)
agente__ = Agent (3, skills__)


agents = [agent, agente_, agente__]

def makePairs(agents, reverse = False):
    """Retorna una asignacion de parejas, de tal forma sean lo mas compatibles posibles de acuerdo a sus skills, o lo mas incompatibles si reverse es True
    Args:
        agents (list of __Agente__): Agentes a emparejar
        reverse (int): Si es verdadero asigna de tal forma que las parejas sean lo mas imcompatibles posibles de acuerdo a sus skills, default: False
    Returns:
        (status, list): (Estado de el solver pulp, Lista de variables pulp con sus resultados)
    """
    problem_title = "Asignacion de parejas"
    skills_ids = agents[0].skills.keys()
    print(reverse)
    objective_type = LpMinimize if reverse else LpMaximize
    prob = LpProblem(problem_title, objective_type) 
    if (len(agents) < 2):
        raise ValueError("If yout want make pairs, please give me more than one agent... ")
    # Complete odd quantity of agents with little skillful agent if want maximize compatibility, with standard agent otherwise
    odd_quantity_of_agents = len(agents) % 2 == 0
    if (not odd_quantity_of_agents and not reverse):
        agents.append(Agent.get_little_skillful_agent(skills_ids))
    if (not odd_quantity_of_agents and reverse):
        agents.append(Agent.get_standard_agent(agents))
    # Si la cantidad de agentes son imapres, se debe crear un agente con id -1 cuyos atributos no interfieran con la asignacion y adicionarlo a agents
    agents_ids = [agent.id for agent in agents]
    agents_dict = {agent.id: agent for agent in agents}
    print(agents_ids)
    agent_pairs = list(itertools.combinations(agents_ids, 2))
    print(agent_pairs)

     
    pairs_assignment = LpVariable.dicts("Asignacion",agent_pairs,None,None,LpBinary)

   
    pair_compatibility = {} # agent_pair: compatibility for the pair
    for agent_pair in agent_pairs:
        agent1 = agents_dict[agent_pair[0]]
        agent2 = agents_dict[agent_pair[1]]
        pair_compatibility[agent_pair] = Agent.get_compatibility(agent1, agent2)
    #Funcion objetivo
    prob += lpSum([pair_compatibility[pair_assignment] * pairs_assignment[pair_assignment] for pair_assignment in pairs_assignment])
    
    #Restricciones
    
    # Cada persona solo puede pertenecer a una pareja
    for agent_id in agents_ids:
        prob += lpSum([pairs_assignment[agent_pair] for agent_pair in agent_pairs if agent_pair[0]==agent_id or agent_pair[1]==agent_id ]) == 1
            
    prob.writeLP("EquilibrioConskills.lp")
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

makePairs(agents, reverse=False)
