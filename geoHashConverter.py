import json
import geohash
from shapely.geometry import Polygon


class GeoHashConverter:

    def __init__(self):
        pass

    def convertPolygonToGeoHash(polygon_geom):

        hashList = geohash.encode(polygon_geom)

        return hashList
