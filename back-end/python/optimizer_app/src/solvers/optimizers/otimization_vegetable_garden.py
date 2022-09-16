import json
import os
from typing import Dict
from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Variable
from entities.Polygon import Polygon
import pandas as pd

class CalculateRectangleVegetableGarden:

    def __init__(self):
        self.__input: Polygon = None
        self._output:Polygon = None
        
        self.number_of_lines: Variable = None
        self.number_of_plants: Variable = None

        self.food_choosen_infos = None
        self.values_solved = {"lines": 0, "plants": 0}
        self.solver = None
        
    def select_food_infos(self) -> Dict:
        return self.__input.plantsSelectedInfos[0]

    def config_solver(self, solver_type: str = "GLOP"):
        self.solver = pywraplp.Solver.CreateSolver(solver_type)   

    def create_variables(self):
        self.number_of_lines = self.solver.IntVar(0,self.solver.infinity(),'lines')
        self.number_of_plants = self.solver.IntVar(0,self.solver.infinity(),'plants')

    def optimization_rules(self):

        #Defining rule to number of lines
        self.solver.Add(
            self.number_of_lines * self.food_choosen_infos["space_between_lines"] <= self.__input.width
        )

        #Defining rule to number of plants
        self.solver.Add(
            self.number_of_plants * self.food_choosen_infos["space_between_plants"] <= self.__input.height
        )

    def define_lines_objetive(self):
        self.solver.Maximize(self.number_of_lines)

    def define_plants_objetive(self):
        self.solver.Maximize(self.number_of_plants)

    def calculate_plants_coordenates_lat_lng(self):
        points = []
        
        for line_index in range(self.values_solved['lines'] +1):
            y_distance = self.food_choosen_infos["space_between_plants"]/2 + line_index*self.food_choosen_infos["space_between_plants"]
        
            for plant_index in range(self.values_solved['plants']+1):
                x_distance = self.food_choosen_infos["space_between_lines"]/2 + plant_index*self.food_choosen_infos["space_between_lines"]
                points.append({"lat": x_distance, "lng": y_distance})

        return points

    def calculate_plants_coordenates_x_y(self):
        x_coordenates = []
        y_coordenates = []
        w = []
        h =[]
        for i in range(self.values_solved['lines']):
            
            for j in range(self.values_solved['plants']):
                x_coordenates.append(j*self.food_choosen_infos['space_between_plants'])
                y_coordenates.append(i*self.food_choosen_infos['space_between_lines'])
                w.append(self.food_choosen_infos['space_between_plants'])
                h.append(self.food_choosen_infos['space_between_lines'])
        df: pd.DataFrame = pd.DataFrame({
                'polygon': self.__input.polygonType,
                'x'   : y_coordenates,
                'y'   : x_coordenates,
                'w'   : w,
                'h'   : h})

        #df.to_csv(f'../results/firstOptimizer/{int(self.__input.width)}.csv', sep=';', decimal=',')
        return df

    def solve(self):
        self.food_choosen_infos = self.select_food_infos()
 
        self.config_solver()
        self.create_variables()
        self.optimization_rules()

        self.define_lines_objetive()
        results_lines = self.solver.Solve()
        
        if results_lines == pywraplp.Solver.OPTIMAL:
            self.values_solved['lines'] = int(self.number_of_lines.solution_value())
        else:
            print('The problem does not have an optimal solution.')
            raise     

        self.define_plants_objetive()
        results_plants = self.solver.Solve()

        if results_plants == pywraplp.Solver.OPTIMAL:
            self.values_solved['plants'] = int(self.number_of_plants.solution_value())
        else:
            print('The problem does not have an optimal solution.')
            raise
        df = self.calculate_plants_coordenates_x_y()
        print(self.values_solved)
        self._output = df


    
    def _set_input(self, input: Polygon):
        self.__input = input

    def get_output(self) -> Dict:
        return self._output


if __name__=="__main__":
    optimizer = CalculateRectangleVegetableGarden()
    optimizer.solve()
    print(optimizer.get_output())