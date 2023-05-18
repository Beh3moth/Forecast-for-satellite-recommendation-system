from geoHashConverter import GeoHashConverter
from meteoThread import MeteoThread


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def start_processing(polygon_geom, queue):
        # the first thing to do is to convert the AOI in a geoHash string
        geohash_converter = GeoHashConverter()

        list_list_geohash = geohash_converter.convert_polygon_to_geohash(polygon_geom)
        print("geohash: ")
        print(list_list_geohash)
        queue.put(list_list_geohash)

        # at this point we can ask for meteo data through the API interface

        # meteo_thread = MeteoThread()
        #
        # meteo_thread.get_dataframe_thread(hash_list, queue)
