import json
import geohash
from shapely.geometry import Polygon


class GeoHashConverter:

    def __init__(self):
        pass

    def convert_polygon_to_geohash(polygon_geom):

        hash_list = geohash.encode(polygon_geom)

        return hash_list
