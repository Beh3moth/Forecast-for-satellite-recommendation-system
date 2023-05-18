import pandas
from openMeteoFetcher import OpenMeteoFetcher
import time
import json


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
                    self.list_data_frame_list[t][i][str(parameter)] = response[i]['hourly'][str(parameter)]
                    temporary_id = 1
                    self.list_data_frame_list[t][i]['AOI_ID'] = temporary_id
                    self.list_data_frame_list[t][i]['EventID'] = temporary_id

    def convert_dataframe_to_json(self):

        list_df_list = []

        for list_dataframe in self.list_data_frame_list:
            df_list = []
            for dataframe in list_dataframe:
                df_list.append(json.loads(dataframe.to_json()))
            list_df_list.append(df_list)

        return str(json.dumps(list_df_list))

    def waiter(self, input_queue, output_queue):

        print("waiter")

        while True:

            list_hash_list = input_queue.get()

            # I have already the resource requested
            if self.list_geohash_list == list_hash_list and self.list_data_frame_list:
                output_queue.put(self.convert_dataframe_to_json())
            else:
                self.list_geohash_list = list_hash_list
                self.list_data_frame_list = []
                for i in range(len(self.list_geohash_list)):
                    self.list_data_frame_list.append([])
                    for j in range(len(self.list_geohash_list[i])):
                        self.list_data_frame_list[i].append(pandas.DataFrame())
                self.update_dataframe()
                output_queue.put(self.convert_dataframe_to_json())

    def updater(self):

        while True:

            print("update")
            if self.list_data_frame_list and self.list_geohash_list:
                self.update_dataframe()
            time.sleep(self.update_hours_interval * 60 * 60)
