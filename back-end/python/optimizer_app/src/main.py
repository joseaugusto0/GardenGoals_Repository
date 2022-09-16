import json
from typing import Dict
import pandas as pd
from solvers.optimizers.first_optimizer import ShelfPacking
from solvers.optimizers.otimization_vegetable_garden import CalculateRectangleVegetableGarden
from solvers.optimizers.circle_bin_packing import CircleBinPacking
from solvers.optimizers.optimizer_with_rbin_pack import RectanglePackerLibOptimizer
from dao.adapters.geometry_functions import RectangleFunctions
from dao.adapters.circle_functions import CircleFunctions
from entities.Polygon import PolygonBuilder
from dao.DAOOutput import DAOOutput
import os
import sys

input = json.loads(sys.argv[1])

#with open('min_input_circle.json', 'r') as f:
#    input = json.load(f)

#rectangle_packing or circle_packing
circle_optimizer_type = "circle_packing"

#first_optm or cm_optim or rect_lib_optm
rectangle_optimizer_type = "rect_lib_optm"

polygonBuilder = PolygonBuilder()
polygonBuilder._set_infos_from_json(input)
polygon = polygonBuilder._get_polygon()

if polygon.polygonType=="rectangle":
    geometryClass = RectangleFunctions()
    geometryClass._set_input(polygon)
    geometryClass._solve_rectangle()
    polygon = geometryClass._get_output()

    if rectangle_optimizer_type=="first_optm":
        rectangleOptimizer = CalculateRectangleVegetableGarden()
    elif rectangle_optimizer_type=="cm_optim":
        rectangleOptimizer = ShelfPacking()
    else:
        rectangleOptimizer = RectanglePackerLibOptimizer()
    

    rectangleOptimizer._set_input(polygon)
    rectangleOptimizer.solve()
    output_optimizer: pd.DataFrame = rectangleOptimizer.get_output()

if polygon.polygonType=="circle":
    if circle_optimizer_type=="rectangle_packing":
        rectangleAdapter = CircleFunctions()
        rectangleAdapter._set_input(polygon)
        rectangleAdapter._solve_circle()

        rectangleOptimizer = RectanglePackerLibOptimizer()
    else:
        rectangleOptimizer = CircleBinPacking()
    
    rectangleOptimizer._set_input(polygon)
    rectangleOptimizer.solve()
    output_optimizer: pd.DataFrame = rectangleOptimizer.get_output()


try:
    print(f"finalResult: {output_optimizer.to_json()}")
except:
    print(f"{polygon}")

    



