from . import resolventes_genericos as resol_genericos
import pulp
import re

class BalancedModelFactory:
    """
    Balanced model factory
    """

    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks
        self.agents_capacities = {}
        self.tasks_costs = {}
        self.agents_capacities = {agent.external_id: agent.capacity for agent in self.agents }
        self.tasks_costs = {task.external_id: task.cost  for task in self.tasks }
    
    def solve(self):
        pulp_status, pulp_variables = resol_genericos.solveEquilibriumProblem(self.agents_capacities, self.tasks_costs)
        assignments = {int(agent):[] for agent in self.agents_capacities.keys()}
        
        for variable in pulp_variables:
            numbers_in_var_name = re.findall(r'\d+', variable.name)
            if (len(numbers_in_var_name) == 2 and variable.varValue == 1):
                agent = int(numbers_in_var_name[0])
                task = int(numbers_in_var_name[1])
                assignments[agent].append(task)
        print(assignments)
        return assignments