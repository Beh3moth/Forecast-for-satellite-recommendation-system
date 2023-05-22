import requests
import geohash
import json


def set_parameters():
    config_file = open('config_simple.json')
    config_parser = json.load(config_file)

    parameter_list = str

    for parameter in config_parser["weatherParameters"]:
        parameter_list = str(parameter_list) + str(parameter) + ","

    parameter_list = parameter_list[:-1]
    parameter_list = parameter_list[13:]

    return parameter_list


def call_api(geohash_list):
    response_list = []

    for el in geohash_list:
        lat, lon = geohash.decode(el)
        parameters = set_parameters()

        # base_url = ("https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude="
        #             + str(lon) + "&hourly=" + str(parameters))

        historical_url = ("https://archive-api.open-meteo.com/v1/archive?latitude=" + str(lat) + "&longitude="
                          + str(lon) + "&start_date=2023-05-03&end_date=2023-05-17&hourly=" + str(parameters))

        response = requests.get(historical_url)
        response = response.json()
        response_list.append(response)
        print("api call")

    return response_list


class OpenMeteoFetcher:

    def __init__(self):
        pass

    @staticmethod
    def get_weather_forecast(geohash_list):
        response = call_api(geohash_list)
        return response
