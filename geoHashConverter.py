import geohash
import numpy as np
import json


class GeoHashConverter:
    update_hours_interval = 0
    geo_hash_dim = 0
    lat_step = 0.1
    lon_step = 0.1

    def __init__(self):
        config_file = open('config.json')
        config_parser = json.load(config_file)
        self.update_hours_interval = config_parser["granularityParameters"]["updateHoursInterval"]

    def compute_total_calls_per_day(self, amount_of_geohash: int):

        # Compute the total amount of calls in a day : a call for each geohash
        total_calls_per_day = amount_of_geohash * (24 / self.update_hours_interval)

        return total_calls_per_day

    # method to set geoHashGranularity. Takes the aoi Polygon as input and evaluates which is the best-fitting
    # granularity of the geohash to be chosen, according to the maximum limit of API calls per day, then sets the
    # geo-hash-dim attribute to that chosen granularity. The higher the geohash granularity, the bigger the number of
    # geo hashes for a given AOI, the bigger the amount of API calls to be made
    def set_geohash_granularity(self, set_polygon):

        aoi_area_size = 0

        for polygon in set_polygon:
            if polygon.area:
                aoi_area_size += polygon.area

        aoi_area_size = aoi_area_size * 111.4 * 111.13

        # Granularity (width, height) in kilometers
        hash_sizes = [(0, 0), (5000000, 5000000), (1250000, 6250000), (156000, 156000), (39100, 19500), (4890, 4890),
                      (1220, 610), (153, 153), (38.2, 19.1), (4.77, 4.77), (1.19, 0.59)]

        hash_area_widths = []

        for pair in hash_sizes:
            hash_area_widths.append((pair[0] * pair[1]) / 10 ** 6)

        # First try with the 6th granularity
        step = 6
        amount_of_geohash = aoi_area_size / hash_area_widths[step]

        tot_calls = self.compute_total_calls_per_day(int(amount_of_geohash))

        # Keep trying more coarse-grained geohash sizes until the amount of total calls is below 10000

        while tot_calls >= 10000 and step > 0:
            # print('iteration')
            step -= 1
            # print("iteration step: " + str(step))
            amount_of_geohash = aoi_area_size / hash_area_widths[step]
            tot_calls = self.compute_total_calls_per_day(int(amount_of_geohash))

        # set chosen granularity to the geo_hash_dim attribute
        if step == 0:
            self.geo_hash_dim = 3
            self.lat_step = hash_sizes[step][0] / 110.574 / 10 ** 3
            self.lon_step = hash_sizes[step][1] / 111.320 / 10 ** 3
        else:
            self.geo_hash_dim = step
            self.lat_step = hash_sizes[step][0] / 110.574 / 10 ** 3
            self.lon_step = hash_sizes[step][1] / 111.320 / 10 ** 3

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

                for lat in np.arange(lat_min, lat_max, self.lat_step / 2):
                    for lon in np.arange(lon_min, lon_max, self.lon_step / 2):
                        geohash_value = geohash.encode(lat, lon, self.geo_hash_dim)
                        geohash_list.add(geohash_value)

                super_set.append(geohash_list)

        return super_set
