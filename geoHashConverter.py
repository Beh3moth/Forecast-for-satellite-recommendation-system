import json
import geopandas
import geohash
from shapely.geometry import Polygon


class GeoHashConverter:
    num_rows = 5
    num_cols = 5
    geo_hash_dim = 2

    def __init__(self):
        config_file = open('config.json')
        config_parser = json.load(config_file)
        self.num_cols = config_parser["granularityParameters"]["granularity"]
        self.num_rows = config_parser["granularityParameters"]["granularity"]

    # def method_fra(self, polygon_geom):
    #     rectangle = geopandas.GeoDataFrame(geometry=geopandas.GeoSeries(polygon_geom).envelope)
    #     return granularity

    def convert_polygon_to_geohash(self, polygon_geom):

        bounds = polygon_geom.bounds()
        lat_min = bounds[1]
        lat_max = bounds[3]
        lon_min = bounds[0]
        lon_max = bounds[2]

        geohash_list = set()

        for lat in range(lat_min, lat_max + 1):
            for lon in range(lon_min, lon_max + 1):
                geohash_value = geohash.encode(lat, lon, self.geo_hash_dim)
                geohash_list.add(geohash_value)

        return geohash_list