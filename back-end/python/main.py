import json
from solvers.optimizers.geometry_functions import GeometryFunctions
from entities.Coordenates import PolygonBuilder
with open("min_input.json", "r") as input:
    min_input: Dict = json.load(input)


polygonBuilder = PolygonBuilder()
polygonBuilder._set_infos_from_json(min_input)
polygon = polygonBuilder._get_polygon()

geometryClass = GeometryFunctions()
geometryClass._set_input(polygon)
geometryClass._get_polygon_to_zero()
polygon = geometryClass._get_output()
