import json
import geohash
from shapely.geometry import Polygon
import numpy as np
from shapely.geometry import MultiPolygon


class GeoHashConverter:

    def __init__(self):
        pass
        # config_file = open('config.json')
        # config_parser = json.load(config_file)



    #method:  Takes the aoi Polygon as input and evaluates which is the best-fitting granularity of the geohash to be
    # to be chosen, according to the maximum limit of API calls per day.
    # The higher the geohash granularity, the bigger the number of geohashes for a given AOI, the bigger the amount
    # of API calls to be made
    def setGeohashGranularity(self, polygon_geom: Polygon):

        def computeTotalCallsPerDay(amountOfGeohashes: int):
            # Set the time frequency of weather updates in a day, as read from the json configuration file.
            config_file = open('config.json')
            config_parser = json.load(config_file)

            hourlyFrequency = config_parser["updateHoursInterval"]
            # Compute the total amount of calls in a day  : a call for each geohash
            totalCallsPerDay = amountOfGeohashes * (24 / hourlyFrequency)

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

    # return chosen granularity
        return step



    # To be changed according to the new approach :  "constructing the geoHash missing strings"
    def convert_polygon_to_geohash(self, polygon_geom: Polygon):

        bounds = polygon_geom.bounds
        lat_min = bounds[1]
        lat_max = bounds[3]
        lon_min = bounds[0]
        lon_max = bounds[2]

        geohash_list = set()

        for lat in np.arange(lat_min, lat_max, 0.1):
            for lon in np.arange(lon_min, lon_max, + 0.1):
                geohash_value = geohash.encode(lat, lon, self.geo_hash_dim)
                geohash_list.add(geohash_value)

        return geohash_list
