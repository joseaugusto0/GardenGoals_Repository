import json
from typing import Dict
import pandas as pd
from solvers.optimizers.first_optimizer import ShelfPacking
from solvers.optimizers.optimizer_with_rbin_pack import RectanglePackerLibOptimizer
from dao.adapters.geometry_functions import RectangleFunctions
from dao.adapters.circle_functions import CircleFunctions
from entities.Polygon import PolygonBuilder
from dao.DAOOutput import DAOOutput
import os
import sys

input = json.loads(sys.argv[1])


polygonBuilder = PolygonBuilder()
polygonBuilder._set_infos_from_json(input)
polygon = polygonBuilder._get_polygon()

if polygon.polygonType=="rectangle":
    geometryClass = RectangleFunctions()
    geometryClass._set_input(polygon)
    geometryClass._solve_rectangle()
    polygon = geometryClass._get_output()

    rectangleOptimizer = RectanglePackerLibOptimizer()
    rectangleOptimizer._set_input(polygon)
    rectangleOptimizer.solve()
    output_optimizer: pd.DataFrame = rectangleOptimizer.get_output()

if polygon.polygonType=="circle":
    circleFuncions = CircleFunctions()
    circleFuncions._set_input(polygon)
    circleFuncions._solve_circle()
    polygon = circleFuncions._get_output()

    rectangleOptimizer = RectanglePackerLibOptimizer()
    rectangleOptimizer._set_input(polygon)
    rectangleOptimizer.solve()
    output_optimizer: pd.DataFrame = rectangleOptimizer.get_output()


try:
    print(f"finalResult: {output_optimizer.to_json()}")
except:
    print(f"{polygon}")

    



