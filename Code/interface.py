from controller import Controller
from input_parser import InputParser


class Interface:
    def __init__(self):
        pass

    # Only method exposed to the other groups. It takes an aoi as input and returns the coordinates.
    # I have specified the type of the aoi and the return's type as str, but it could be different or omitted.
    # There could be also the need of some kind of check on the aoi (it could be empty ecc).
    # this method is static because it doesn't modify any instance or class attributes.
    @staticmethod
    def get_weather_forecast(json_aoi, queue, parameter_list):

        # Create the controller
        controller = Controller()
        input_parser = InputParser()

        # Call the method of the controller that takes the aoi as input and returns the final output.
        controller.start_processing(input_parser.get_multipolygon(json_aoi), queue, json_aoi, parameter_list)
