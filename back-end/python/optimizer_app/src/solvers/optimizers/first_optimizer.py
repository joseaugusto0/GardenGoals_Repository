from ast import Dict, List
import time
import math
from ortools.sat.python import cp_model
from ortools.linear_solver.pywraplp import Variable
import pandas
import json
import os
from entities.Polygon import Polygon
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#---------------------------------------------------
# data 
#---------------------------------------------------

class ShelfPacking:
    def __init__(self):
        self.__input: Polygon = None
        self._output:Polygon = None

        self.n_rectangles: int = 0
        self.actives: Dict[str,Variable] = {}
        self.x = None

        self.food_infos = None
        self.rectangles_ordered = None
        self.areas = None
        self.solver = None

        #Parameters variables
        self.bin_H: int = None
        self.bin_W: int = None
        self.items_h: List[int] = None
        self.items_w: List[int] = None
        self.n_items: int = None
        self.garden_area: int = None
        self.plant_areas: int = None

        #Optimizer variables
        self.xb1: List[Variable] = None
        self.xb2: List[Variable] = None
        self.y2: List[Variable] = None
        
        #Optimizer variables - NoOverlap2D auxiliar variables
        self.xival: List[Variable] = None
        self.yival: List[Variable] = None

        #Optimizer variable - Objective
        self.z: List[Variable] = None

        #Optimizer variables - Output
        self.b: List[Variable] = None #Bin numbers
        self.x: List[Variable] = None #X coordenates numbers
        self.y1: List[Variable] = None #Y coordenates numbers



    def select_food_infos(self) -> Dict:
        measurements = json.load(open(f"{os.path.dirname(os.path.abspath(__file__))}/sizes.json"))
        return measurements

    def _get_bin_dims(self):

        self.bin_H = int(self.__input.height)
        self.bin_W = int(self.__input.width)
        self.garden_area = self.bin_H*self.bin_W

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
        self.plant_areas = sum([list(*food.values())[0]*list(*food.values())[1] for food in self.rectangles_ordered])

        # h,w,cat for each item
        self.items_h = [list(*food.values())[0] for food in self.rectangles_ordered for _ in range(math.floor((self.garden_area/self.plant_areas)*0.8))]
        self.items_w = [list(*food.values())[1] for food in self.rectangles_ordered for _ in range(math.floor((self.garden_area/self.plant_areas)*0.8))]

        self.n_items = len(self.items_h)
        self.m = 1

    def config_solver(self):
        self.solver = cp_model.CpModel()

    def get_vars(self):
        #self.active = [self.solver.NewIntVar(0,1,f'active{i}') for i in range(self.n_items)]
        self.x = [self.solver.NewIntVar(0,self.bin_W-self.items_w[i],f'x{i}') for i in range(self.n_items)]
        
        self.xb1 = [self.solver.NewIntVar(0,self.bin_W-self.items_w[i],f'xb1.{i}') for i in range(self.n_items)]
        self.xb2 = [self.solver.NewIntVar(self.items_w[i],self.bin_W,f'xb2.{i}') for i in range(self.n_items)]

        self.y1 = [self.solver.NewIntVar(0,self.bin_H-self.items_h[i],f'y1.{i}') for i in range(self.n_items)]
        self.y2 = [self.solver.NewIntVar(self.items_h[i],self.bin_H,f'y2.{i}') for i in range(self.n_items)]

        # interval variables
        self.xival = [self.solver.NewIntervalVar(self.xb1[i],self.items_w[i],self.xb2[i],f'xival{i}') for i in range(self.n_items)]
        self.yival = [self.solver.NewIntervalVar(self.y1[i],self.items_h[i],self.y2[i],f'yival{i}') for i in range(self.n_items)]
        
        # bin numbers
        self.b = [self.solver.NewIntVar(0,self.m-1,f'b{i}') for i in range(self.n_items)]

        # objective
        self.z = self.solver.NewIntVar(0,self.m-1,'z')

    def set_constraints(self):
        for i in range(self.n_items):
            self.solver.Add(self.xb1[i] == self.x[i] + self.b[i]*self.bin_W)
            self.solver.Add(self.xb2[i] == self.xb1[i] + self.items_w[i])

        self.solver.AddNoOverlap2D(self.xival,self.yival)

        self.solver.AddMaxEquality(self.z,[self.b[i] for i in range(self.n_items)])

        self.solver.Minimize(self.z) 

    def solve(self):
        start_time = time.time()
        self.config_solver()
        self._get_bin_dims()
        self.sort_desc_rectangles_by_height()
        self._get_dims_from_items()
        self.get_vars()
        self.set_constraints()

        solver = cp_model.CpSolver()
        solver.parameters.log_search_progress = True
        solver.parameters.num_search_workers = 8
        rc = solver.Solve(self.solver) 
        print(f"return code:{rc}")
        print(f"status:{solver.StatusName()}")

        
        if rc == 4:
            
            df: pandas.DataFrame = pandas.DataFrame({ 
                'polygon': self.__input.polygonType,
                'x'   : [solver.Value(self.x[i]) for i in range(self.n_items)],
                'y'   : [solver.Value(self.y1[i]) for i in range(self.n_items)],
                'h'   : self.items_w,
                'w'   : self.items_h})

           
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

            self._output = df      
        
    def _set_input(self, input: Polygon):
        self.__input = input

    def get_output(self) -> Dict:
        return self._output

