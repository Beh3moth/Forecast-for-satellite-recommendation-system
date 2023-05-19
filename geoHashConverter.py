import geohash
import numpy as np
import json
from shapely.geometry import multipolygon

    
class GeoHashConverter:

    def __init__(self):
        config_file = open('config.json')
        config_parser = json.load(config_file)

        self.update_hours_interval = config_parser["granularityParameters"]["updateHoursInterval"]



    # method to set geoHashGranularity. Takes the aoi Polygon as input and evaluates which is the best-fitting granularity of the geohash
    # to be chosen, according to the maximum limit of API calls per day, then sets the geo-hash-dim attribute to that
    # chosen granularity.
    # The higher the geohash granularity, the bigger the number of geohashes for a given AOI, the bigger the amount
    # of API calls to be made
    def setGeohashGranularity(self, polygon_geom: multipolygon):    #TODO: check how to handle a multipolygon as input

        def computeTotalCallsPerDay(amountOfGeohashes: int):

            # Compute the total amount of calls in a day  : a call for each geohash
            totalCallsPerDay = amountOfGeohashes * (24 / self.update_hours_interval)

            return totalCallsPerDay

        rectangle = geopandas.GeoDataFrame(geometry=geopandas.GeoSeries(polygon_geom).envelope)

        rectangle.to_crs({'init': 'epsg: 3857'})   # needed to convert to a Cartesian system projection
        aoiAreaSize = rectangle.area / 10 ** 6                   # obtain the area in square kms

        # Granularity (width, height) in kilometers
        hashSizes = [(0, 0), (5000000, 5000000), (1250000, 6250000), (156000, 156000), (39100, 19500), (4890, 4890),
                     (1220, 610), (153, 153), (38.2, 19.1), (4.77, 4.77), (1.19, 0.59)]

        hashAreaWidths = []

        for pair in hashSizes:
            hashAreaWidths.append(pair[0]*pair[1])

        # First try with the 6th granularity
        step = 6;
        amountOfGeohashes = aoiAreaSize / hashAreaWidths[step]

        totCalls = computeTotalCallsPerDay(amountOfGeohashes)
        # Keep trying more coarse-grained geohash sizes until the amount of total calls is below 10000
        while (totCalls >= 10000 and step > 0):
            step -= 1
            amountOfGeohashes = aoiAreaSize / hashAreaWidths[step]

    # set chosen granularity to the geo_hash_dim attribtue
        self.geo_hash_dim = step



    #TODO: To be changed according to the new approach :  "constructing the geoHash missing strings"
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
