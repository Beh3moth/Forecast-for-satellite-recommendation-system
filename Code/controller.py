from geoHashConverter import GeoHashConverter
import json
import datetime



# Reads the maximumApiCalls from the config file and the current counter of calls from the logger
# and returns True if the current amount of calls performed exceeds the daily threshold, False otherwise.
def is_amount_of_calls_exceeded():

    # Read the JSON logging file
    data = json.load(open("../Memory/calls_log.json"))

    # Get the current date
    current_date = datetime.date.today().strftime('%Y-%m-%d')

    # checks if the date has to be reset wrt the last record saved in the log file
    if data.get('date') != current_date:
        data['date'] = current_date
        data['counter'] = 0

    # get the current amount of calls in the log
    current_calls = data['counter']

    # get the daily calls threshold
    config_file = open('../Memory/config_simple.json')
    config_parser = json.load(config_file)
    daily_calls_threshold = config_parser["granularityParameters"]["maximumApiCalls"]

    if current_calls >= daily_calls_threshold:
        return True



def modify_parameter(parameter_list):
    with open("../Memory/config_parameter.json") as json_file:
        data = json.load(json_file)
    data['weatherParameters'] = parameter_list
    updated_json = json.dumps(data, indent=4)
    with open('../Memory/config_parameter.json', 'w') as file:
        file.write(updated_json)



class Controller:

    def __init__(self):
        pass


    @staticmethod
    def start_processing(polygon_geom, queue, info, parameter_list):

        # First let's check if the amount of API calls in the logger exceeds the daily threshold of calls
        if is_amount_of_calls_exceeded():
            # TODO: print ERROR MESSAGE in the output queue

        # Else, start the processing by setting the geohash granularity and converting the AOI in geoHash strings
        else:
            geohash_converter = GeoHashConverter()

            geohash_converter.set_geohash_granularity(polygon_geom)
            list_list_geohash = geohash_converter.convert_polygon_to_geohash(polygon_geom)
            queue.put(list_list_geohash)
            queue.put(info)
            modify_parameter(parameter_list)
