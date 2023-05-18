import pandas
from openMeteoFetcher import OpenMeteoFetcher
import time
import json
import threading
import asyncio


class MeteoThread:
    list_data_frame_list = []
    openMeteoFetcher = OpenMeteoFetcher()
    list_geohash_list = set()
    update_hours_interval = 3

    def __init__(self):
        config_file = open('config.json')
        config_parser = json.load(config_file)
        self.update_hours_interval = config_parser["granularityParameters"]["updateHoursInterval"]

    def update_dataframe(self):

        for t, hashlist in enumerate(self.list_geohash_list):
            response = self.openMeteoFetcher.get_weather_forecast(hashlist)
            for i in range(len(self.list_geohash_list[t])):
                for parameter in response[i]['hourly']:
                    # print("Measures:")
                    # print(i)
                    # print(len(self.list_data_frame_list[t][i]))
                    # print(len(self.list_data_frame_list[t]))
                    self.list_data_frame_list[t][i][str(parameter)] = response[i]['hourly'][str(parameter)]
                    temporary_id = 1
                    self.list_data_frame_list[t][i]['AOI_ID'] = temporary_id
                    self.list_data_frame_list[t][i]['EventID'] = temporary_id


    def convert_dataframe_to_json(self):

        print("warning")
        print(len(self.list_data_frame_list))

        list_df_list = []

        for list_dataframe in self.list_data_frame_list:
            df_list = []
            for dataframe in list_dataframe:
                df_list.append(json.loads(dataframe.to_json()))
            list_df_list.append(df_list)

        return str(json.dumps(list_df_list))

    def get_dataframe_thread(self, input_queue, output_queue):

        while True:

            self.list_geohash_list = input_queue.get()
            self.list_data_frame_list = []
            for i in range(len(self.list_geohash_list)):
                self.list_data_frame_list.append([])
                for j in range(len(self.list_geohash_list[i])):
                    self.list_data_frame_list[i].append(pandas.DataFrame())
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
