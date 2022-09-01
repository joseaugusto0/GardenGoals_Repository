from ast import Dict
from entities.Polygon import Polygon
from matplotlib import pyplot as plt

class DAOOutput:
    def __init__(self):
        self.__input: Polygon = None
        self._output: Polygon = None

    def _visualize_rectangle_with_plants(self):

        plt.plot([x['lat'] for x in self.__input.rectangle_optimized.plants_coordenates], [y['lng'] for y in self.__input.rectangle_optimized.plants_coordenates], marker = "o",linewidth = 0, color='green')
        plt.show()
        pass


    def _set_input(self, input: Polygon):
        self.__input = input

    def get_output(self) -> Dict:
        return self._output