from geoHashConverter import GeoHashConverter
import json

def modify_parameter(parameter_list):
    with open("config_parameter.json") as json_file:
        data = json.load(json_file)
    data['weatherParameters'] = parameter_list
    updated_json = json.dumps(data, indent=4)
    with open('config_parameter.json', 'w') as file:
        file.write(updated_json)

class Controller:
    def __init__(self):
        pass

    @staticmethod
    def start_processing(polygon_geom, queue, info, parameter_list):
        # the first thing to do is to convert the AOI in a geoHash string
        geohash_converter = GeoHashConverter()

        geohash_converter.set_geohash_granularity(polygon_geom)
        list_list_geohash = geohash_converter.convert_polygon_to_geohash(polygon_geom)
        queue.put(list_list_geohash)
        queue.put(info)
        modify_parameter(parameter_list)
