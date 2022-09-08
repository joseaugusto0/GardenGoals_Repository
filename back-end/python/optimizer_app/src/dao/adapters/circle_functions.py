from entities.Polygon import Polygon, PolygonBuilder
import math

class CircleFunctions:

    def __init__(self):

        self.__input: Polygon = None
        self._output: Polygon = PolygonBuilder()._get_polygon()
        self._polygon_coordenates_in_zero = []

    def _get_circumscribed_rectangle_into_circle(self):
        self.__input.width = math.sqrt(2*(self.__input.radius)**2)
        self.__input.height = self.__input.width

    def _solve_circle(self):
        self._get_circumscribed_rectangle_into_circle()
        
        self._output = self.__input
        print(self._output)
        

    def _set_input(self, input: Polygon):
        self.__input = input
        self._output.polygonType = input.polygonType

    def _get_output(self) -> Polygon:
        return self._output
