from shapely import MultiPolygon
from shapely.geometry import shape


class InputParser:

    @staticmethod
    def get_date(input_aoi):
        input_aoi["date"] = input_aoi["features"][0]["properties"]["date"]
        date = str(input_aoi["date"]).split(" ")[0]
        day = date.split('-')[2]
        month = date.split('-')[1]
        year = date.split('-')[0]
        return day, month, year

    @staticmethod
    def get_coordinates(json_aoi):
        return json_aoi['features'][0]['geometry']['coordinates']

    def get_multipolygon(self, json_aoi):

        if json_aoi['features'][0]["geometry"]["type"] == "Polygon":
            polygon = shape({"type": "Polygon", "coordinates": self.get_coordinates(json_aoi)})
            multipolygon = MultiPolygon([polygon])
            multipolygon = multipolygon.geoms
        else:
            # Create a Shapely MultiPolygon object
            multipolygon = shape({"type": "MultiPolygon", "coordinates": self.get_coordinates(json_aoi)})
            multipolygon = MultiPolygon(multipolygon)
            multipolygon = multipolygon.geoms
            # Call the method of the controller that takes the aoi as input and returns the final output.
        return multipolygon
