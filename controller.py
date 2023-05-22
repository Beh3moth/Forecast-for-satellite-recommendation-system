from geoHashConverter import GeoHashConverter


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def start_processing(polygon_geom, queue):
        # the first thing to do is to convert the AOI in a geoHash string
        geohash_converter = GeoHashConverter()

        geohash_converter.set_geohash_granularity(polygon_geom)
        list_list_geohash = geohash_converter.convert_polygon_to_geohash(polygon_geom)
        queue.put(list_list_geohash)
