import geohash
import numpy as np
import json
from shapely.geometry import multipolygon
import geopandas


class GeoHashConverter:

    update_hours_interval = 0
    geo_hash_dim = 0

    def __init__(self):
        config_file = open('config.json')
        config_parser = json.load(config_file)
        self.update_hours_interval = config_parser["granularityParameters"]["updateHoursInterval"]

    def compute_total_calls_per_day(self, amount_of_geohash: int):

        # Compute the total amount of calls in a day  : a call for each geohash
        total_calls_per_day = amount_of_geohash * (24 / self.update_hours_interval)

        return total_calls_per_day

    # method to set geoHashGranularity. Takes the aoi Polygon as input and evaluates which is the best-fitting
    # granularity of the geohash to be chosen, according to the maximum limit of API calls per day, then sets the
    # geo-hash-dim attribute to that chosen granularity. The higher the geohash granularity, the bigger the number of
    # geo hashes for a given AOI, the bigger the amount of API calls to be made
    def set_geohash_granularity(self, polygon_geom: multipolygon):  # TODO: check how to handle a multipolygon as input

        rectangle = geopandas.GeoSeries(geopandas.GeoSeries(polygon_geom).envelope)

        # rectangle.to_crs({'init': 'epsg: 3857'})  # needed to convert to a Cartesian system projection
        aoi_area_size = rectangle.area / 10 ** 6  # obtain the area in square kms

        # Granularity (width, height) in kilometers
        hash_sizes = [(0, 0), (5000000, 5000000), (1250000, 6250000), (156000, 156000), (39100, 19500), (4890, 4890),
                     (1220, 610), (153, 153), (38.2, 19.1), (4.77, 4.77), (1.19, 0.59)]

        hash_area_widths = []

        for pair in hash_sizes:
            hash_area_widths.append(pair[0] * pair[1])

        # First try with the 6th granularity
        step = 6
        amount_of_geohash = aoi_area_size / hash_area_widths[step]

        tot_calls = self.compute_total_calls_per_day(amount_of_geohash)
        # Keep trying more coarse-grained geohash sizes until the amount of total calls is below 10000

        while tot_calls >= 10000 and step > 0:
            step -= 1
            amount_of_geohash = aoi_area_size / hash_area_widths[step]
            tot_calls = self.compute_total_calls_per_day(amount_of_geohash)

        # set chosen granularity to the geo_hash_dim attribute
        self.geo_hash_dim = step

    # TODO: To be changed according to the new approach :  "constructing the geoHash missing strings"
    def convert_polygon_to_geohash(self, multi_polygon):

        super_set = []

        for polygon in multi_polygon:

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
