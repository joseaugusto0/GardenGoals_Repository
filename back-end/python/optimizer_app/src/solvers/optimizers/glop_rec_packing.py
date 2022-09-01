from ast import Dict, Tuple
import json
from entities.Polygon import Polygon
from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Variable

class GLOPRectanglePacking:
    def __init__(self):
        self.__input: Polygon = None
        self._output:Polygon = None

        self.n_rectangles: int = 0
        self.actives: Dict[str,Variable] = {}
        self.xi: Dict[Tuple(str,int,int), int] = {}
        self.yi: Dict[Tuple(str,int,int), int] = {}
        self.xf: Dict[Tuple(str,int,int), int] = {}
        self.yf: Dict[Tuple(str,int,int), int] = {}

        self._test_width = 200
        self._test_height = 300

        self.max_width: int = None
        self.max_height: int = None

        self.food_infos = self.select_food_infos()
        self.rectangles_ordered = None
        self.areas = None
        self.solver = None
        
    def select_food_infos(self) -> Dict:
        measurements = json.load(open('./solvers/optimizers/sizes.json'))
        return measurements

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
           
        return rectangles_rotated_and_desc_ordered

    def select_polygons(self):
        print(self.rectangles_ordered)
        raise
        if self.__input.width>=self.__input.height:
            for food_name,i in self.food_infos.items():
                print(food_name)
                raise
        elif self.__input.width<self.__input.height:
            self.sort_desc_rectangles_by_height()

    def config_solver(self, solver_type: str = "SCIP"):
        self.solver = pywraplp.Solver.CreateSolver(solver_type) 
        self.solver.EnableOutput()   

    def config_values(self):
        #Interacting through all (x,y) in area
        for x in range(0, self.max_width):
            for y in range(0, self.max_height):

                for food in self.rectangles_ordered:
                    key = str(*food.keys()),x, y
                    var_name = f"{str(*food.keys())}_{x}_{y}"
                    self.actives[key] = self.solver.IntVar(0,1, var_name)
                    self.xi[key] = list(*food.values())[1]
                    self.yi[key] = list(*food.values())[0]
                    self.xf[key] = x + list(*food.values())[1]
                    self.yf[key] = y + list(*food.values())[0]

    def defining_rules(self):
        #Interacting through all cm in area
        for y in range(0, self.max_height-1):
            for x in range(0, self.max_width-1):
                if y==0 and x==0:
                    key = str(*self.rectangles_ordered[0].keys()),x, y
                    self.solver.Add(
                        self.actives[key]==1
                    )
                    continue
                
                for food_i in self.rectangles_ordered:
                    key_previous = str(*food_i.keys()),(x), (y)
                    for food_f in self.rectangles_ordered:
                        key = str(*food_f.keys()),x+1, y
                        
                        self.solver.Add(
                            self.actives[key]*self.xi[key] >= self.actives[key_previous]*self.xi[key_previous] 
                        )
                        self.solver.Add(
                            self.actives[key]*self.xi[key] >= (self.actives[key_previous]*self.xi[key_previous] + list(*food_i.values())[1]-1)
                        )

                    #self.solver.Add(
                    #    self.actives[key]*self.ys[key] >= self.actives[key_previous]*self.ys[key_previous]
                    #)
                    #self.solver.Add(
                    #    self.actives[key]*self.ys[key] >= (self.actives[key_previous]*self.ys[key_previous] + list(*food.values())[0]-1)
                    #)

    def objective(self):
        obj = []
        for k in self.actives:
            obj.append(self.actives[k])
        self.solver.Maximize(self.solver.Sum(obj))


    def solve(self):
        self.rectangles_ordered = self.sort_desc_rectangles_by_height()
        self.n_rectangles = len(self.rectangles_ordered)

        self.config_solver()
        self.config_values()
        self.defining_rules()
        self.objective()

        status = self.solver.Solve()
        
        if status == pywraplp.Solver.OPTIMAL:
            print('Solucao:')
            print(f'Funcao objetivo ={self.solver.Objective().Value()}')
            raise

            for y in range(0, self.max_height-1):
                for x in range(0, self.max_width-1):
                    for food_i in self.rectangles_ordered:
                        key = str(*food_i.keys()),x, y
                        if self.actives[key].solution_value()==1:
                            print(self.actives)
        raise

        

        

        # The objective is the sum of the areas of all included rectangles
        obj = Sum([actives[i] * areas[i] for i in range(n)])
        s.maximize(obj)
        s.check()
        
    def _set_input(self, input: Polygon):
        self.__input = input

    def get_output(self) -> Dict:
        return self._output