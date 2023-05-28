import requests
import geohash
import json
import pandas
from logger import Logger


def set_parameters():
    config_file = open('../Memory/config_simple.json')
    config_parser = json.load(config_file)

    parameter_list = str

    for parameter in config_parser["weatherParameters"]:
        parameter_list = str(parameter_list) + str(parameter) + ","

    parameter_list = parameter_list[:-1]
    parameter_list = parameter_list[13:]

    return parameter_list


# Add an "is_day" column to the DataFrame and set its initial value to 1.
def add_is_day(dataframe):

    dataframe["is_day"] = 1

    # Define a condition
    condition = pandas.to_datetime(dataframe["time"]).dt.hour > 18

    # Update the selected positions with a new value
    dataframe.loc[condition, 'is_day'] = 0

    return dataframe


def convert_response_in_dataframe(response_list):
    response_list = [response_list]
    dataframe_list = []
    for i, response in enumerate(response_list):
        dataframe_list.append(pandas.DataFrame(response[0]['hourly']))
        dataframe_list[i] = add_is_day(dataframe_list[i])
    return dataframe_list


def call_api(geohash_list, day, month, year):
    response_list = []
    logger = Logger()

    for el in geohash_list:
        lat, lon = geohash.decode(el)
        parameters = set_parameters()

        # base_url = ("https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude="
        #             + str(lon) + "&hourly=" + str(parameters))

        historical_url = ("https://archive-api.open-meteo.com/v1/archive?latitude=" + str(lat) + "&longitude="
                          + str(lon) + "&start_date=" + year + "-" + month + "-" + day + "&end_date=" + year + "-"
                          + month + "-" + str(int(day) + 6) + "&hourly=" + str(parameters))

        logger.add_call()

        response = requests.get(historical_url)
        response = response.json()
        response_list.append(response)

    return response_list


class OpenMeteoFetcher:

    def __init__(self):
        pass

    @staticmethod
    def get_weather_forecast(geohash_list, day, month, year):
        response = call_api(geohash_list, day, month, year)
        return convert_response_in_dataframe(response)
