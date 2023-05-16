import json
from shapely import Polygon
from controller import Controller


class Interface:
    def __init__(self):
        pass

    @staticmethod
    # Only method exposed to the other groups. It takes an aoi as input and returns the coordinates.
    # I have specified the type of the aoi and the return's type as str, but it could be different or omitted.
    # There could be also the need of some kind of check on the aoi (it could be empty ecc).
    # this method is static because it doesn't modify any instance or class attributes.
    def get_weather_forecast(aoi):
        # conversion in json?
        # json_aoi = json.loads(aoi)
        # Check on the aoi?

        # Create the controller
        controller = Controller()

        # Call the method of the controller that takes the aoi as input and returns the final output.
        return controller.start_processing(aoi)
