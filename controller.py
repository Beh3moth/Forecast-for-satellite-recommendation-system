import json
from geoHashConverter import GeoHashConverter
from dataHistory import DataHistory
from openMeteoFetcher import OpenMeteoFetcher


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def start_processing(polygon_geom):
        # the first thing to do is to convert the AOI in a geoHash string
        geohash_converter = GeoHashConverter()

        hash_list = geohash_converter.convert_polygon_to_geohash(polygon_geom)

        print(hash_list)

        # at this point we can ask for meteo data through the API interface

        api = OpenMeteoFetcher()

        response = api.get_weather_forecast(hash_list)

        # at this point we can create the DataHistory class initiating its geo data frame
        data_history = DataHistory(response)

        output = 1

        return output
