from ast import Dict, List
import time
import math
from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Variable
import pandas
import json
import os
from entities.Polygon import Polygon
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from gurobipy import *

#---------------------------------------------------
# data 
#---------------------------------------------------

class CircleBinPacking:
    def __init__(self):
        self.__input: Polygon = None
        self._output:Polygon = None

        self.n_rectangles: int = 0
        self.actives: Dict[str,Variable] = {}
        self.x = None

        self.food_infos = None
        self.rectangles_ordered = None
        self.areas = None
        self.solver: Model = None

        #Parameters variables
        self.bin_H: int = None
        self.bin_W: int = None
        self.items_h: List[int] = None
        self.items_w: List[int] = None
        self.n_items: int = None
        self.garden_area: int = None
        self.plant_areas: int = None

        #Optimizer variables
        self.x: List[Variable] = None
        self.y: List[Variable] = None

        #Optimizer variable - Objective
        self.z: List[Variable] = None

        #Optimizer variables - Output
        self.b: List[Variable] = None #Bin numbers
        self.x: List[Variable] = None #X coordenates numbers
        self.y1: List[Variable] = None #Y coordenates numbers

    def sort_desc_rectangles_by_height(self, orientation_selected: str = "height"):
        rectangles_rotated_and_desc_ordered = []

        min_height = None
        min_width = None
        
        for food_info in self.__input.plantsSelectedInfos:

            if not min_height and not min_width:
                min_height = food_info["space_between_lines"]
                min_width = food_info["space_between_plants"]
            else:
                if food_info["space_between_lines"] < min_height:
                    min_height = food_info["space_between_lines"]
                if food_info["space_between_plants"] < min_width:  
                    min_width =  food_info["space_between_plants"]
            
            rectangles_rotated_and_desc_ordered.append({
                f"{food_info['name']}": [
                    food_info["space_between_lines"],
                    food_info["space_between_plants"]
                ]
            })

        aux = None
        for rectangle in range(len(rectangles_rotated_and_desc_ordered)-1):
            for rectangle_to_compare in range(rectangle,len(rectangles_rotated_and_desc_ordered)):
                if rectangle_to_compare==rectangle:
                    continue
                else:
                    if list(*rectangles_rotated_and_desc_ordered[rectangle_to_compare].values())[0]>list(*rectangles_rotated_and_desc_ordered[rectangle].values())[0]:
                        aux = rectangles_rotated_and_desc_ordered[rectangle]
                        rectangles_rotated_and_desc_ordered[rectangle] = rectangles_rotated_and_desc_ordered[rectangle_to_compare]
                        rectangles_rotated_and_desc_ordered[rectangle_to_compare] = aux
           

        self.rectangles_ordered = rectangles_rotated_and_desc_ordered

    def _get_dims_from_items(self):
        self.plant_areas = sum([math.pi*(list(*food.values())[1]/2)**2 for food in self.rectangles_ordered])
        self.garden_area = math.pi*(self.__input.radius**2)

        self.items_radius = [int(list(*food.values())[1]/2) for food in self.rectangles_ordered for _ in range(math.floor((self.garden_area/self.plant_areas)*0.7))]
        self.n_items = len(self.items_radius)

    def config_solver(self):
        self.solver = Model('quadratic')   
        self.solver.setParam('OutputFlag', True)
        self.solver.setParam('NonConvex', 2)
        #self.solver.setParam('TimeLimit', 10)

    def get_vars(self):

        self.x = [self.solver.addVar(
            vtype=GRB.INTEGER,
            lb=-self.__input.radius/2,
            ub=self.__input.radius/2,
            name = f'x_{i}') for i in range(self.n_items)]
        self.y = [self.solver.addVar(
            vtype=GRB.INTEGER,
            lb=-self.__input.radius/2,
            ub=self.__input.radius/2,
            name=f'y_{i}') for i in range(self.n_items)]

    def set_constraints(self):
        
        for i in range(self.n_items):
            for j in range(self.n_items):
                if i==j:
                    continue
                self.solver.addConstr(
                    (self.x[i] - self.x[j])**2 + (self.y[i] - self.y[j])**2
                    >= (self.items_radius[i] + self.items_radius[j])**2
                )
                self.solver.addConstr(
                    (self.x[i])**2 + (self.y[i])**2
                    <= (self.__input.radius - self.items_radius[i])**2
                )


    def solve(self):
        start_time = time.time()
        self.config_solver()
        self.sort_desc_rectangles_by_height()
        self._get_dims_from_items()
        self.get_vars()
        self.set_constraints()
        self.solver.optimize()
        
        if self.solver.getVars():

            df: pandas.DataFrame = pandas.DataFrame({
                'polygon': self.__input.polygonType,
                'x': [i.x for i in self.x],
                'y': [i.x for i in self.y],
                'item_radius': [i for i in self.items_radius],
            })

            '''_, ax = plt.subplots()
            plt.xlim([-self.__input.radius/2, self.__input.radius/2])
            plt.ylim([-self.__input.radius/2, self.__input.radius/2])
            ax.add_patch(Circle((0, 0), self.__input.radius/2, color='#EB70AA'))
            for _,row in df.iterrows():
                
                if row['item_radius']==list(*self.rectangles_ordered[0].values())[1]:
                    color = '#0099FF'
                #elif row['item_radius']==list(*self.rectangles_ordered[1].values())[1]:
                #    color = '#EB70AA'
                #elif row['item_radius']==list(*self.rectangles_ordered[2].values())[1]:
                #    color = '#FFF000'
                ax.add_patch(Circle((row['x'], row['y']), row['item_radius']))'''
            
            plt.show()
            
            self._output = df
        else:
            return False


        
        '''if rc == 4:
            
            df: pandas.DataFrame = pandas.DataFrame({ 
                'bin' : [solver.Value(self.b[i]) for i in range(self.n_items)],
                'y'   : [solver.Value(self.x[i]) for i in range(self.n_items)],
                'x'   : [solver.Value(self.y1[i]) for i in range(self.n_items)],
                'w'   : self.items_w,
                'h'   : self.items_h})

           
            _, ax = plt.subplots()
            plt.scatter(x=self.bin_W, y=self.bin_H)

            
            for _,row in df.iterrows():
                
                if row['w']==list(*self.rectangles_ordered[0].values())[1]:
                    color = '#0099FF'
                elif row['w']==list(*self.rectangles_ordered[1].values())[1]:
                    color = '#EB70AA'
                elif row['w']==list(*self.rectangles_ordered[2].values())[1]:
                    color = '#FFF000'
                ax.add_patch(Rectangle((row['x'], row['y']), row['w'], row['h'],edgecolor = 'black', facecolor=color))

            self._output = df      '''
        
    def _set_input(self, input: Polygon):
        self.__input = input

    def get_output(self) -> Dict:
        return self._output

