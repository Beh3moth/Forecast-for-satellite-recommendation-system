import geohash
from shapely.geometry import Polygon
import numpy as np


class GeoHashConverter:

    geo_hash_dim = 2

    def __init__(self):
        pass
        # config_file = open('config.json')
        # config_parser = json.load(config_file)

    # def method_fra(self, polygon_geom):
    #     rectangle = geopandas.GeoDataFrame(geometry=geopandas.GeoSeries(polygon_geom).envelope)
    #     return granularity

    def convert_polygon_to_geohash(self, multipolygon):

        super_set = []

        for polygon in multipolygon:

            if polygon.area:

                bounds = polygon.bounds
                lat_min = bounds[1]
                lat_max = bounds[3]
                lon_min = bounds[0]
                lon_max = bounds[2]

                geohash_list = set()

                for lat in np.arange(lat_min, lat_max, 0.1):
                    for lon in np.arange(lon_min, lon_max, + 0.1):
                        geohash_value = geohash.encode(lat, lon, self.geo_hash_dim)
                        geohash_list.add(geohash_value)
                super_set.append(geohash_list)

        return super_set
