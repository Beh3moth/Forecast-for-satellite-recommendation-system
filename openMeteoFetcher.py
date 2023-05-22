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


def call_api(geohash_list, day, month, year):
    response_list = []

    for el in geohash_list:
        lat, lon = geohash.decode(el)
        parameters = set_parameters()

        # base_url = ("https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude="
        #             + str(lon) + "&hourly=" + str(parameters))

        historical_url = ("https://archive-api.open-meteo.com/v1/archive?latitude=" + str(lat) + "&longitude="
                          + str(lon) + "&start_date=" + year + "-" + month + "-" + day + "&end_date=" + year + "-"
                          + month + "-" + str(int(day) + 7) + "&hourly=" + str(parameters))

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
        return response
