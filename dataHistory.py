import geopandas as gp


class DataHistory:

    geo_data_frame = gp.GeoDataFrame()

    def __init__(self, hash_list):
        self.geo_data_frame['geometry'] = hash_list


