from controller import Controller
from shapely import MultiPolygon
from shapely.geometry import shape


class Interface:
    def __init__(self):
        pass

    @staticmethod
    def add_event_info(json_aoi):
        info = {}
        info["eventId"] = json_aoi["features"][0]["properties"]["eventId"]
        info["eventType"] = json_aoi["features"][0]["properties"]["eventType"]
        info["lat"] = json_aoi["features"][0]["properties"]["lat"]
        info["long"] = json_aoi["features"][0]["properties"]["long"]
        date = str(json_aoi["features"][0]["properties"]["date"])
        info["day"] = date.split('-')[0]
        info["month"] = date.split('-')[1]
        info["year"] = date.split('-')[2]
        return info

    # Only method exposed to the other groups. It takes an aoi as input and returns the coordinates.
    # I have specified the type of the aoi and the return's type as str, but it could be different or omitted.
    # There could be also the need of some kind of check on the aoi (it could be empty ecc).
    # this method is static because it doesn't modify any instance or class attributes.
    def get_weather_forecast(self, json_aoi, queue):

        coordinates = json_aoi['features'][0]['geometry']['coordinates']

        # Create a Shapely MultiPolygon object
        multipolygon = shape({"type": "MultiPolygon", "coordinates": coordinates})
        multipolygon = MultiPolygon(multipolygon)
        multipolygon = multipolygon.geoms

        # Create the controller
        controller = Controller()

        # Call the method of the controller that takes the aoi as input and returns the final output.
        controller.start_processing(multipolygon, queue, self.add_event_info(json_aoi))
