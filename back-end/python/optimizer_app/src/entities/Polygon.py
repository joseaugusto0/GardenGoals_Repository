from typing import Dict, List
from entities.RectangleOptimized import RectangleOptimized, RectangleOptimizedBuilder

class Polygon:
    def __init__(self):
        self.polygonType: str = None
        self.coordenates: List[Dict[float]]
        self.polygonToZero: List[Dict[float]] = None
        self.width: float = None #cm
        self.height: float = None #cm
        self.area: float = None #cm2
        self.radius: float = None
        self.rectangle_optimized:RectangleOptimized = None
        self.plantsSelectedInfos: List[Dict] = []

    def __repr__(self):
        res = '\n'
        for field, value in self.__dict__.items():
            res += str(field) + ':\n ' + str(value).replace('\n', '\n\t')
            res += '\n'
        res += '\n'
        return res

class PolygonBuilder:
    def __init__(self):
        self.polygon: Polygon = Polygon()

    def _set_infos_from_json(self, infos: dict):
        self.polygon.polygonType = infos['polygon']
        self.polygon.coordenates = infos['coordenates']
        if width:=infos['width']:
            self.polygon.width = width
        if height:=infos['height']:
            self.polygon.height = height
        self.polygon.radius = infos['radius']

        for plant in infos['plantInfos']:
            if plant:
                self.polygon.plantsSelectedInfos.append(plant)

    def _get_polygon(self) -> Polygon:
        return self.polygon



