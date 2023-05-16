import json
import geohash
from shapely.geometry import Polygon


class GeoHashConverter:

    def __init__(self):
        pass

    @staticmethod
    def convert_polygon_to_geohash(polygon_geom):

        hash_list = set()

        coordinates = polygon_geom.exterior.coords.xy
        latitudes = coordinates[1]
        longitudes = coordinates[0]

        for lat, lon in zip(latitudes, longitudes):
            hash_list.add(geohash.encode(lat, lon))

        return hash_list
