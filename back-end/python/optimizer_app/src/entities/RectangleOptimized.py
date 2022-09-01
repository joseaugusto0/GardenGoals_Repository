
from typing import Dict


class RectangleOptimized:
    def __init__(self):
        self.number_of_lines: float = None
        self.number_of_plants: float = None
        self.plants_coordenates: Dict = None

    def __repr__(self):
        res = '\n'
        for field, value in self.__dict__.items():
            res += str(field) + ':\n ' + str(value).replace('\n', '\n\t')
            res += '\n'
        res += '\n'
        return res

class RectangleOptimizedBuilder:
    def __init__(self):
        self.rectangle_optimized: RectangleOptimized = RectangleOptimized()

    def _set_infos_from_json(self, infos: dict):
        self.rectangle_optimized.number_of_lines = infos['lines']
        self.rectangle_optimized.number_of_plants = infos['plants']

    def _get_rectangle_optimized(self) -> RectangleOptimized:
        return self.rectangle_optimized



