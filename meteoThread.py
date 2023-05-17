import threading

import pandas
import pandas as pd
from openMeteoFetcher import OpenMeteoFetcher
import time
import json
import asyncio


class MeteoThread:
    data_frame_list = []
    openMeteoFetcher = OpenMeteoFetcher()
    geohash_list = set()
    update_hours_interval = 3

    def __init__(self):
        config_file = open('config.json')
        config_parser = json.load(config_file)
        self.update_hours_interval = config_parser["granularityParameters"]["updateHoursInterval"]

    # def get_dataframe(self, geohash_list):
    #
    #     self.geohash_list = geohash_list
    #
    #     for i in range(len(self.geohash_list)):
    #         self.data_frame_list.append(pandas.DataFrame())
    #
    #     # condition for updating the dataframe
    #     response = self.openMeteoFetcher.get_weather_forecast(self.geohash_list)
    #
    #     for i in range(len(self.data_frame_list)):
    #         for parameter in response[i]['hourly']:
    #             self.data_frame_list[i][str(parameter)] = response[i]['hourly'][str(parameter)]
    #             temporary_id = 1
    #             self.data_frame_list[i]['AOI_ID'] = temporary_id
    #             self.data_frame_list[i]['EventID'] = temporary_id
    #
    #     return self.data_frame_list

    def update_dataframe(self):

        # condition for updating the dataframe
        response = self.openMeteoFetcher.get_weather_forecast(self.geohash_list)

        for i in range(len(self.data_frame_list)):
            for parameter in response[i]['hourly']:
                self.data_frame_list[i][str(parameter)] = response[i]['hourly'][str(parameter)]
                temporary_id = 1
                self.data_frame_list[i]['AOI_ID'] = temporary_id
                self.data_frame_list[i]['EventID'] = temporary_id

    def get_dataframe_thread(self, geohash_list, queue):

        while True:

            # if the geohash_list of the class is null then initialize it and the dataframe list
            if not self.geohash_list:
                self.geohash_list = geohash_list
                for i in range(len(self.geohash_list)):
                    self.data_frame_list.append(pandas.DataFrame())

            self.update_dataframe()
            queue.put(self.data_frame_list)
            time.sleep(3 * 60 * 60)
