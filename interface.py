from controller import Controller
import json
from shapely import Polygon
from shapely import MultiPolygon
from shapely.geometry import shape


class Interface:
    def __init__(self):
        pass

    @staticmethod
    # Only method exposed to the other groups. It takes an aoi as input and returns the coordinates.
    # I have specified the type of the aoi and the return's type as str, but it could be different or omitted.
    # There could be also the need of some kind of check on the aoi (it could be empty ecc).
    # this method is static because it doesn't modify any instance or class attributes.
    def get_weather_forecast(json, queue):
        coordinates = json['features'][0]['geometry']['coordinates']

        # Create a Shapely MultiPolygon object
        multipolygon = shape({"type": "MultiPolygon", "coordinates": coordinates})
        multipolygon = MultiPolygon(multipolygon)
        multipolygon = multipolygon.geoms

        # Create the controller
        controller = Controller()

        # Call the method of the controller that takes the aoi as input and returns the final output.
        controller.start_processing(multipolygon[0], queue)
