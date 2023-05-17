import requests
import geohash
import json


def set_parameters():

    config_file = open('config.json')
    config_parser = json.load(config_file)

    parameter_list = str

    for parameter in config_parser["weatherParameters"]:
        parameter_list = str(parameter_list) + str(parameter) + str(",")

    parameter_list = parameter_list[:-1]

    return parameter_list


def call_api(geohash_list):
    response_list = []

    for el in geohash_list:
        lat, lon = geohash.decode(el)

        parameters = set_parameters()
        print(parameters)
        base_url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(lon) + "&hourly=" + str(parameters)
        response = requests.get(base_url)
        response = response.json()
        response_list.append(response)

    return response_list


class OpenMeteoFetcher:

    def __init__(self):
        pass

    @staticmethod
    def get_weather_forecast(geohash_list):
        response = call_api(geohash_list)
        return response
