from ast import Dict, Tuple
from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Variable
import pandas
import json
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

        self._test_width = 200
        self._test_height = 300

        self.max_width: int = None
        self.max_height: int = None

        self.food_infos = self.select_food_infos()
        self.rectangles_ordered = None
        self.areas = None
        self.solver = None

        self.bin_H = None
        self.bin_W = None
        self.items_h = None
        self.items_w = None
        self.n_items = None

    def select_food_infos(self) -> Dict:
        measurements = json.load(open('./solvers/optimizers/sizes.json'))
        return measurements

    def _get_bin_dims(self):
        self.bin_H = int(self.__input.height)
        self.bin_W = int(self.__input.width)

    def sort_desc_rectangles_by_height(self, orientation_selected: str = "height"):
        rectangles_rotated_and_desc_ordered = []

        min_height = None
        min_width = None
        for food_name,i in self.food_infos.items():

            if not min_height and not min_width:
                min_height = self.food_infos[food_name]["space between lines"]
                min_width = self.food_infos[food_name]["space between plants"]
            else:
                if self.food_infos[food_name]["space between lines"] < min_height:
                    min_height = self.food_infos[food_name]["space between lines"]
                if self.food_infos[food_name]["space between plants"] < min_width:  
                    min_width =  self.food_infos[food_name]["space between plants"]
            
            rectangles_rotated_and_desc_ordered.append({
                f"{food_name}": [
                    self.food_infos[food_name]["space between lines"],
                    self.food_infos[food_name]["space between plants"]
                ]
            })
        
        self.max_height = int(self._test_height) - int(min_height) 
        self.max_width = int(self._test_width) - int(min_width) 

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
        self.n_items = 30  # number of items

        # h,w,cat for each item
        self.items_h = [list(*food.values())[0] for food in self.rectangles_ordered for _ in range(self.n_items)]
        self.items_w = [list(*food.values())[1] for food in self.rectangles_ordered for _ in range(self.n_items)]

        self.n_items = len(self.items_h)

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
        self.b = [self.solver.NewIntVar(0,1,f'b{i}') for i in range(self.n_items)]

        # objective
        self.z = self.solver.NewIntVar(0,1,'z')


    def set_constraints(self):
        for i in range(self.n_items):
            self.solver.Add(self.xb1[i] == self.x[i] + self.b[i]*self.bin_W)
            self.solver.Add(self.xb2[i] == self.xb1[i] + self.items_w[i])

        self.solver.AddNoOverlap2D(self.xival,self.yival)

        self.solver.AddMaxEquality(self.z,[self.b[i] for i in range(self.n_items)])

        self.solver.Minimize(self.z) 

    def solve(self):
        self.config_solver()
        self._get_bin_dims()
        self.sort_desc_rectangles_by_height()
        self._get_dims_from_items()
        self.get_vars()
        self.set_constraints()

        solver = cp_model.CpSolver()
        solver.parameters.log_search_progress = True
        solver.parameters.max_time_in_seconds = 10.0
        rc = solver.Solve(self.solver)
        print(f"return code:{rc}")
        print(f"status:{solver.StatusName()}")
        print(self.bin_H)
        print(self.bin_W)

        
        if rc == 4 or rc == 3:
            
            
            df: pandas.DataFrame = pandas.DataFrame({ 
                'bin' : [solver.Value(self.b[i]) for i in range(self.n_items)],
                'x'   : [solver.Value(self.x[i]) for i in range(self.n_items)],
                'y'   : [solver.Value(self.y1[i]) for i in range(self.n_items)],
                'w'   : self.items_w,
                'h'   : self.items_h})

            
            
            fig, ax = plt.subplots()
            plt.scatter(x=self.bin_H, y=self.bin_W)

            cont = 0
            colors = {
                '0': '#0099FF',
                '1': '#EB70AA',
                '2': '#FFF000'
            }
            for _,row in df.iterrows():
                ax.add_patch(Rectangle((row['x'], row['y']), row['w'], row['h'], color=colors[f'{cont}']))
                if cont==2:
                    cont=0
                else:
                    cont += 1

            plt.show()
        raise
        
    def _set_input(self, input: Polygon):
        self.__input = input

    def get_output(self) -> Dict:
        return self._output

