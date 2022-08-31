import json
from typing import Dict
from solvers.optimizers.optimizer_shelf_packing import ShelfPacking
from solvers.optimizers.geometry_functions import GeometryFunctions
from entities.Polygon import PolygonBuilder
from dao.DAOOutput import DAOOutput

with open("min_input.json", "r") as input:
    min_input: Dict = json.load(input)


polygonBuilder = PolygonBuilder()
polygonBuilder._set_infos_from_json(min_input)
polygon = polygonBuilder._get_polygon()

geometryClass = GeometryFunctions()
geometryClass._set_input(polygon)
geometryClass._solve_rectangle()
polygon = geometryClass._get_output()

if polygon.polygonType=="rectangle":
    rectangleOptimizer = ShelfPacking()
    rectangleOptimizer._set_input(polygon)
    rectangleOptimizer.solve()
    polygon = rectangleOptimizer.get_output()

dao_output = DAOOutput()
dao_output._set_input(polygon)
dao_output._visualize_rectangle_with_plants()



