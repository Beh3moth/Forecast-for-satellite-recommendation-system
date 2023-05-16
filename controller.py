import json
from geoHashConverter import GeoHashConverter


class Controller:
    def __init__(self):
        pass

    def startTheProcessingMethod(polygon_geom):

        # the first thing to do is to convert the AOI in a geoHash string
        geoHashConverter = GeoHashConverter()

        hashList = geoHashConverter.convertPolygonToGeoHash(polygon_geom)

        output = aoi
        return output



    # at this point we can create the DataHistory class

    # at this point we can ask for meteo data through the API interface

