import json
import os
from typing import Dict
from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Variable

class CalculateVegetableGarden:

    def __init__(self, food: str = 'lettuce', width: int = 100, lenght: int = 200):
        self.number_of_lines: Variable = None
        self.number_of_plants: Variable = None
        print(os.listdir())
        self.measurements = json.load(open('sizes.json'))
        self.food_choosen_infos = self.select_food_infos(food)
        self.solver = None
        self.width = width #cm
        self.lenght = lenght #cm
        self.output = {
            "Lines": 0,
            "Plants": 0
        }

    def select_food_infos(self, food: str) -> Dict:
        return self.measurements[food]

    def config_solver(self, solver_type: str = "GLOP"):
        self.solver = pywraplp.Solver.CreateSolver(solver_type)   

    def create_variables(self):
        self.number_of_lines = self.solver.IntVar(0,self.solver.infinity(),'lines')
        self.number_of_plants = self.solver.IntVar(0,self.solver.infinity(),'plants')

    def optimization_rules(self):

        #Defining rule to number of lines
        reference = self.food_choosen_infos["width max"]*.85 if self.food_choosen_infos["width max"]>self.food_choosen_infos["space between lines"] else self.food_choosen_infos["space between lines"]
        self.solver.Add(
            self.number_of_lines * reference <= self.width
        )

        #Defining rule to number of plants
        reference = self.food_choosen_infos["width max"]*.85 if self.food_choosen_infos["width max"]>self.food_choosen_infos["space between plants"] else self.food_choosen_infos["space between plants"]
        self.solver.Add(
            self.number_of_plants * reference <= self.lenght
        )

    def define_lines_objetive(self):
        self.solver.Maximize(self.number_of_lines)

    def define_plants_objetive(self):
        self.solver.Maximize(self.number_of_plants)

    def solve(self):

        self.config_solver()
        self.create_variables()
        self.optimization_rules()

        self.define_lines_objetive()
        results_lines = self.solver.Solve()

        if results_lines == pywraplp.Solver.OPTIMAL:
            self.output['Lines'] = self.number_of_lines.solution_value()
        else:
            print('The problem does not have an optimal solution.')
            raise     

        self.define_plants_objetive()
        results_plants = self.solver.Solve()

        if results_plants == pywraplp.Solver.OPTIMAL:
            self.output['Plants'] = self.number_of_plants.solution_value()
        else:
            print('The problem does not have an optimal solution.')
            raise
    
    def get_output(self):
        return self.output

optimizer = CalculateVegetableGarden()
optimizer.solve()
print(optimizer.get_output())