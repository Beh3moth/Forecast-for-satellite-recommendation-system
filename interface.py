from controller import Controller
from shapely import MultiPolygon
from shapely import Polygon
from shapely.geometry import shape


class Interface:
    def __init__(self):
        pass

    # @staticmethod
    # def add_event_info(json_aoi):
    #     info = {}
    #     info["eventId"] = json_aoi["features"][0]["properties"]["eventId"]
    #     info["eventType"] = json_aoi["features"][0]["properties"]["eventType"]
    #     info["lat"] = json_aoi["features"][0]["properties"]["lat"]
    #     info["long"] = json_aoi["features"][0]["properties"]["long"]
    #     info["date"] = json_aoi["features"][0]["properties"]["date"]
    #     date = str(json_aoi["features"][0]["properties"]["date"])
    #     info["day"] = date.split('-')[0]
    #     info["month"] = date.split('-')[1]
    #     info["year"] = date.split('-')[2]
    #     return info

    # Only method exposed to the other groups. It takes an aoi as input and returns the coordinates.
    # I have specified the type of the aoi and the return's type as str, but it could be different or omitted.
    # There could be also the need of some kind of check on the aoi (it could be empty ecc).
    # this method is static because it doesn't modify any instance or class attributes.
    @staticmethod
    def get_weather_forecast(json_aoi, queue, parameter_list):

        # Create the controller
        controller = Controller()

        coordinates = json_aoi['features'][0]['geometry']['coordinates']

        if json_aoi['features'][0]["geometry"]["type"] == "Polygon":
            polygon = shape({"type": "Polygon", "coordinates": coordinates})
            multipolygon = MultiPolygon([polygon])
            multipolygon = multipolygon.geoms
            controller.start_processing(multipolygon, queue, json_aoi, parameter_list)
        else:
            # Create a Shapely MultiPolygon object
            multipolygon = shape({"type": "MultiPolygon", "coordinates": coordinates})
            multipolygon = MultiPolygon(multipolygon)
            multipolygon = multipolygon.geoms
            # Call the method of the controller that takes the aoi as input and returns the final output.
            controller.start_processing(multipolygon, queue, json_aoi, parameter_list)



