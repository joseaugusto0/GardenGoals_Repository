from typing import Dict, List

class Polygon:
    def __init__(self):
        self.polygonType: str = None
        self.coordenates: List[Dict[float]]
        self.polygonToZero: List[Dict[float]] = None
        self.width: float = None #cm
        self.height: float = None #cm
        self.area: float = None #cm2

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

    def _get_polygon(self) -> Polygon:
        return self.polygon



