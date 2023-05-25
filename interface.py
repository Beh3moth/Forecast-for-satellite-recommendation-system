from controller import Controller
from shapely import MultiPolygon
from shapely.geometry import shape


class Interface:
    def __init__(self):
        pass

    # Only method exposed to the other groups. It takes an aoi as input and returns the coordinates.
    # I have specified the type of the aoi and the return's type as str, but it could be different or omitted.
    # There could be also the need of some kind of check on the aoi (it could be empty ecc).
    # this method is static because it doesn't modify any instance or class attributes.
    @staticmethod
    def get_weather_forecast(json_aoi, queue):

        # Create the controller
        controller = Controller()

        coordinates = json_aoi['features'][0]['geometry']['coordinates']

        if json_aoi['features'][0]["geometry"]["type"] == "Polygon":
            polygon = shape({"type": "Polygon", "coordinates": coordinates})
            multipolygon = MultiPolygon([polygon])
            multipolygon = multipolygon.geoms
            controller.start_processing(multipolygon, queue, json_aoi)
        else:
            # Create a Shapely MultiPolygon object
            multipolygon = shape({"type": "MultiPolygon", "coordinates": coordinates})
            multipolygon = MultiPolygon(multipolygon)
            multipolygon = multipolygon.geoms
            # Call the method of the controller that takes the aoi as input and returns the final output.
            controller.start_processing(multipolygon, queue, json_aoi)
