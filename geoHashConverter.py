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

    def get_centroids(self, polygon_geom):

        rectangle = geopandas.GeoDataFrame(geometry=geopandas.GeoSeries(polygon_geom).envelope)

        # Define the number of rows and columns for the grid
        num_rows = self.num_rows
        num_cols = self.num_cols

        # Calculate the width and height of each sub-area
        width = (rectangle.bounds['maxx'] - rectangle.bounds['minx']) / num_cols
        height = (rectangle.bounds['maxy'] - rectangle.bounds['miny']) / num_rows

        # Create an empty list to store the sub-areas
        sub_areas = []

        # Iterate over the rows and columns to create the grid of sub-areas
        for row in range(num_rows):
            for col in range(num_cols):
                minx = rectangle.bounds['minx'] + col * width
                maxx = minx + width
                miny = rectangle.bounds['miny'] + row * height
                maxy = miny + height
                sub_area_coords = [(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)]
                sub_areas.append(Polygon(sub_area_coords))

        # Create a GeoDataFrame with the sub-areas
        sub_areas_gdf = geopandas.GeoDataFrame(geometry=sub_areas)

        # Perform the spatial intersection to obtain the divided sub-areas
        divided_areas = geopandas.overlay(sub_areas_gdf, rectangle, how='intersection')

        centroids = set()

        for index, row in divided_areas.iterrows():
            if polygon_geom.intersects(row.geometry).bool():
                centroids.add(row.geometry.centroid)

        return centroids

    def convert_polygon_to_geohash(self, polygon_geom):

        hash_list = set()

        centroids = self.get_centroids(polygon_geom)

        for centroid in centroids:
            hash_list.add(geohash.encode(centroid.y, centroid.x, self.geo_hash_dim))

        return hash_list
