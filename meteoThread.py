import pandas
from openMeteoFetcher import OpenMeteoFetcher
import time
import json
import threading
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

    def update_dataframe(self):

        # condition for updating the dataframe
        response = self.openMeteoFetcher.get_weather_forecast(self.geohash_list)

        for i in range(len(self.data_frame_list)):
            for parameter in response[i]['hourly']:
                self.data_frame_list[i][str(parameter)] = response[i]['hourly'][str(parameter)]
                temporary_id = 1
                self.data_frame_list[i]['AOI_ID'] = temporary_id
                self.data_frame_list[i]['EventID'] = temporary_id

    def convert_dataframe_to_json(self):

        print("warning")
        print(len(self.data_frame_list))

        df_list = []

        for dataframe in self.data_frame_list:
            df_list.append(json.loads(dataframe.to_json()))

        return str(df_list)

    def get_dataframe_thread(self, input_queue, output_queue):

        while True:

            self.geohash_list = input_queue.get()
            self.data_frame_list = []
            for i in range(len(self.geohash_list)):
                self.data_frame_list.append(pandas.DataFrame())
            self.update_dataframe()
            output_queue.put(self.convert_dataframe_to_json())


        # while True:
        #
        #     print('ciclo iniziato')
        #
        #     geohash_list = set()
        #
        #     # expected to find the hash_list
        #     if not input_queue.empty():
        #         print("queue con qualcosa")
        #         geohash_list = input_queue.get()
        #     elif self.geohash_list:
        #         print("update")
        #         self.update_dataframe()
        #
        #     # if the geohash_list of the class is not null then initialize it and the dataframe list
        #     if (geohash_list and not self.data_frame_list) or self.geohash_list != geohash_list:
        #         print("hash mai vista")
        #         self.geohash_list = geohash_list
        #         self.data_frame_list = []
        #         for i in range(len(self.geohash_list)):
        #             self.data_frame_list.append(pandas.DataFrame())
        #         self.update_dataframe()
        #         print("messo nella queue")
        #         output_queue.put(self.convert_dataframe_to_json())
        #     elif self.geohash_list == geohash_list and self.data_frame_list:
        #         print("hash già vista e ho già i dati")
        #         output_queue.put(self.convert_dataframe_to_json())
        #
        #     print('a nanna')
        #     time.sleep(10)
