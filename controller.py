import json
from geoHashConverter import GeoHashConverter


class Controller:
    def __init__(self):
        pass

    def start_processing(polygon_geom):

        # the first thing to do is to convert the AOI in a geoHash string
        geohash_converter = GeoHashConverter()

        hash_list = geohash_converter.convert_polygon_to_geohash(polygon_geom)

        output = 1

        return output



    # at this point we can create the DataHistory class

    # at this point we can ask for meteo data through the API interface

