import json
from geoHashConverter import GeoHashConverter
from meteoThread import MeteoThread
import asyncio
import time
import threading
import queue


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def start_processing(polygon_geom):
        # the first thing to do is to convert the AOI in a geoHash string
        geohash_converter = GeoHashConverter()

        hash_list = geohash_converter.convert_polygon_to_geohash(polygon_geom)

        # at this point we can ask for meteo data through the API interface

        meteo_thread = MeteoThread()

        return meteo_thread.get_dataframe(hash_list)
