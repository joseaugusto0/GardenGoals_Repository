from typing import Dict
from entities.Polygon import Polygon, PolygonBuilder
from matplotlib import pyplot as plt


class GeometryFunctions:

    def __init__(self):

        self.__input: Polygon = None
        self._output: Polygon = PolygonBuilder()._get_polygon()
        self._polygon_coordenates_in_zero = []

    def _find_point_closest_to_zero(self) -> Dict[float, float]:
        minor_x_value = None
        minor_y_value = None
        closest_to_zero = None
        cont = 0

        for j in self.__input.coordenates:
            if cont==0:
                minor_x_value = abs(j['lat'])
                minor_y_value = abs(j['lng'])
                cont += 1
                
            if abs(j['lat'])<=minor_x_value and abs(j['lng'])<=minor_y_value:
                minor_x_value = j['lat']
                minor_y_value = j['lng']
                closest_to_zero = {"lat":j['lat'], "lng":j['lng']}

        return closest_to_zero

    def _get_polygon_to_zero(self):
        
        closest_to_zero = self._find_point_closest_to_zero()
        x_difference = abs(closest_to_zero['lat'])
        y_difference = abs(closest_to_zero['lng'])

        for coordenate in self.__input.coordenates:
            self._polygon_coordenates_in_zero.append({"lat": coordenate['lat']-x_difference,"lng": coordenate['lng']-y_difference})

        #self._show_polygon(self._polygon_coordenates_in_zero)

        self._output.coordenates = self.__input.coordenates
        self._output.polygonToZero = self._polygon_coordenates_in_zero
        
    def _show_polygon(self, coordenates: Dict):
        plt.plot([x['lat'] for x in coordenates], [y['lng'] for y in coordenates], marker = "o")
        plt.show()

    def _organizing_rectangle_points(self):
        # first: origin
        # second: down/right
        # third: up/right
        # fourth: up/left
        self._output.polygonToZero = [
            *[coord for coord in self._output.polygonToZero if coord['lat']==0 and coord['lng']==0],
            *[coord for coord in self._output.polygonToZero if coord['lat']==0 and coord['lng']!=0],
            *[coord for coord in self._output.polygonToZero if coord['lat']!=0 and coord['lng']!=0],
            *[coord for coord in self._output.polygonToZero if coord['lat']==0 and coord['lng']!=0],
        ]

    def _get_width_and_height(self):
        #Fixing Google Maps Scale Level 13 : 72223.822090
        scale_level = 72223.822090
        self._output.width = (self._output.polygonToZero[1]['lat']-self._output.polygonToZero[0]['lat'])*scale_level
        self._output.height = (self._output.polygonToZero[3]['lng']-self._output.polygonToZero[0]['lng'])*scale_level
    def _solve_rectangle(self):
        self._get_polygon_to_zero()
        self._organizing_rectangle_points()
        self._get_width_and_height()

    def _set_input(self, input: Polygon):
        self.__input = input
        self._output.polygonType = input.polygonType

    def _get_output(self) -> Polygon:
        return self._output
