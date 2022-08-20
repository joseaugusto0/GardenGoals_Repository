import json
import os
from typing import Dict
from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Variable
from entities.Polygon import Polygon
from entities.RectangleOptimized import RectangleOptimizedBuilder

class CalculateRectangleVegetableGarden:

    def __init__(self, food: str = 'lettuce'):
        self.__input: Polygon = None
        self._output:Polygon = None
        
        self.number_of_lines: Variable = None
        self.number_of_plants: Variable = None

        self.food_choosen_infos = self.select_food_infos(food)
        self.values_solved = {"lines": 0, "plants": 0}
        self.solver = None
        
    def select_food_infos(self, food: str) -> Dict:
        measurements = json.load(open('./solvers/optimizers/sizes.json'))
        return measurements[food]

    def config_solver(self, solver_type: str = "GLOP"):
        self.solver = pywraplp.Solver.CreateSolver(solver_type)   

    def create_variables(self):
        self.number_of_lines = self.solver.IntVar(0,self.solver.infinity(),'lines')
        self.number_of_plants = self.solver.IntVar(0,self.solver.infinity(),'plants')

    def optimization_rules(self):

        #Defining rule to number of lines
        reference = self.food_choosen_infos["width max"]*.85 if self.food_choosen_infos["width max"]>self.food_choosen_infos["space between lines"] else self.food_choosen_infos["space between lines"]
        self.solver.Add(
            self.number_of_lines * reference <= self.__input.width
        )

        #Defining rule to number of plants
        reference = self.food_choosen_infos["width max"]*.85 if self.food_choosen_infos["width max"]>self.food_choosen_infos["space between plants"] else self.food_choosen_infos["space between plants"]
        self.solver.Add(
            self.number_of_plants * reference <= self.__input.height
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
            self.values_solved['lines'] = self.number_of_lines.solution_value()
        else:
            print('The problem does not have an optimal solution.')
            raise     

        self.define_plants_objetive()
        results_plants = self.solver.Solve()

        if results_plants == pywraplp.Solver.OPTIMAL:
            self.values_solved['plants'] = self.number_of_plants.solution_value()
        else:
            print('The problem does not have an optimal solution.')
            raise

        
        rectangle_optimized_builder = RectangleOptimizedBuilder()
        rectangle_optimized_builder._set_infos_from_json(self.values_solved)
        self.__input.rectangle_optimized = rectangle_optimized_builder._get_rectangle_optimized()
        self._output = self.__input

    
    def _set_input(self, input: Polygon):
        self.__input = input

    def get_output(self) -> Dict:
        return self._output


if __name__=="__main__":
    optimizer = CalculateRectangleVegetableGarden()
    optimizer.solve()
    print(optimizer.get_output())