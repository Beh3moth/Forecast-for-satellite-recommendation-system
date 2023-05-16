import geopandas
import geohash
from shapely.geometry import Polygon
from shapely.geometry import Point
import geopandas.tools as tools


class GeoHashConverter:
    
    num_rows = 5
    num_cols = 5

    def __init__(self):
        pass

    def convert_polygon_to_geohash(self, polygon_geom):

        hash_list = set()

        x = geopandas.GeoSeries(polygon_geom)
              
        rectangle = geopandas.GeoDataFrame(geometry=x.envelope)

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
            if(polygon_geom.intersects(row.geometry).bool()==True):
                centroids.add(row.geometry.centroid)
    
        for centroid in centroids:
            hash_list.add(geohash.encode(centroid.y, centroid.x, 2))

        return hash_list
