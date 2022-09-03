import json
from typing import Dict
import pandas as pd
from solvers.optimizers.first_optimizer import ShelfPacking
from solvers.optimizers.geometry_functions import GeometryFunctions
from entities.Polygon import PolygonBuilder
from dao.DAOOutput import DAOOutput
import os
import sys

input = json.loads(sys.argv[1])


polygonBuilder = PolygonBuilder()
polygonBuilder._set_infos_from_json(input)
polygon = polygonBuilder._get_polygon()


geometryClass = GeometryFunctions()
geometryClass._set_input(polygon)
geometryClass._solve_rectangle()
polygon = geometryClass._get_output()


if polygon.polygonType=="rectangle":
    rectangleOptimizer = ShelfPacking()
    rectangleOptimizer._set_input(polygon)
    rectangleOptimizer.solve()
    output_optimizer: pd.DataFrame = rectangleOptimizer.get_output()
    print(polygon)

try:
    print(f"finalResult: {output_optimizer.to_json()}")
except:
    print(f"{polygon}")

    



