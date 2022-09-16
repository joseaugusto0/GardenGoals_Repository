from ast import Dict, List
import time
import math
from ortools.linear_solver.pywraplp import Variable
import pandas
import inspect
import rpack
from entities.Polygon import Polygon
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


#---------------------------------------------------
# data 
#---------------------------------------------------

class RectanglePackerLibOptimizer:
    def __init__(self):
        self.__input: Polygon = None
        self._output:Polygon = None

        self.rectangles_ordered = None

        #Parameters variables
        self.bin_H: int = None
        self.bin_W: int = None
        self.items_h: List[int] = None
        self.items_w: List[int] = None
        self.n_items: int = None
        self.garden_area: int = None
        self.plant_areas: int = None

        self.bin_dim = 1


    def _get_bin_dims(self):

        self.bin_H = int(self.__input.height)
        self.bin_W = int(self.__input.width)

        #self.bin_H = self.bin_dim
        #self.bin_W = self.bin_dim

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
            
            rectangles_rotated_and_desc_ordered.append((
                    food_info["space_between_lines"],
                    food_info["space_between_plants"]
                )
            )


        aux = None
        for rectangle in range(len(rectangles_rotated_and_desc_ordered)-1):
            for rectangle_to_compare in range(rectangle,len(rectangles_rotated_and_desc_ordered)):
                if rectangle_to_compare==rectangle:
                    continue
                else:

                    if rectangles_rotated_and_desc_ordered[rectangle_to_compare][0]>rectangles_rotated_and_desc_ordered[rectangle][0]:
                        aux = rectangles_rotated_and_desc_ordered[rectangle]
                        rectangles_rotated_and_desc_ordered[rectangle] = rectangles_rotated_and_desc_ordered[rectangle_to_compare]
                        rectangles_rotated_and_desc_ordered[rectangle_to_compare] = aux

        self.rectangles_ordered = rectangles_rotated_and_desc_ordered #(y,x)


        self.plant_areas = sum([food[0]*food[1] for food in rectangles_rotated_and_desc_ordered])
        
        all_rectangles = []
        for _ in range(math.floor((self.garden_area/self.plant_areas)*0.95)):
            for rec_type in range(len(rectangles_rotated_and_desc_ordered)):
                all_rectangles.append(rectangles_rotated_and_desc_ordered[rec_type])
        
        self.rects = all_rectangles

    def solve(self):

        start_time = time.time()
        self._get_bin_dims()
        self.sort_desc_rectangles_by_height()

        results = None
        try:
            results = rpack.pack(self.rects, self.bin_W, self.bin_H)
        except Exception as er:
            problem_inspect = inspect.getmembers(er, lambda a: not(inspect.isroutine(a)))
            results = problem_inspect[-1][1][1]

            #    print(er)


        if results:

            all_positions = []
            for item_index in range(len(results)):
                infos = { 
                    'polygon': self.__input.polygonType,
                    'optimizer_type': "rectangle_packing",
                    'y'   : results[item_index][1],
                    'x'   : results[item_index][0],
                    'w'   : self.rects[item_index][1],
                    'h'   : self.rects[item_index][0]}

                all_positions.append(infos)

            df = pandas.DataFrame(all_positions)  
            self._output = df
            #df.to_csv(f'./solvers/optimizers/results/sheets/bin_{self.bin_dim}.csv', sep=';', decimal=',')  

            
            #fig, ax = plt.subplots()
            #plt.scatter(self.bin_W, self.bin_H)
            
            #for _,row in df.iterrows():
                
            #    if row['w']==self.rectangles_ordered[0][1]:
            #        color = '#0099FF'
            #    elif row['w']==self.rectangles_ordered[1][1]:
            #        color = '#EB70AA'

            #    ax.add_patch(Rectangle((row['x'], row['y']), row['w'], row['h'],edgecolor = 'black'))

            #plt.savefig(f'./solvers/optimizers/results/images/bin_{self.bin_dim}.png')
            #plt.cla()
            #plt.close(fig)
            #plt.show()
        

        
    def _set_input(self, input: Polygon):
        self.__input = input

    def get_output(self) -> Dict:
        return self._output

