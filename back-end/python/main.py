import json
from typing import Dict
from solvers.optimizers.geometry_functions import GeometryFunctions
from solvers.optimizers.otimization_vegetable_garden import CalculateRectangleVegetableGarden
from entities.Polygon import PolygonBuilder

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
    rectangleOptimizer = CalculateRectangleVegetableGarden()
    rectangleOptimizer._set_input(polygon)
    rectangleOptimizer.solve()
    print(rectangleOptimizer.get_output())


