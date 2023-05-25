import pandas
from openMeteoFetcher import OpenMeteoFetcher
import time
import json
from input_parser import InputParser


class MeteoThread:

    # Handy initialization
    list_data_frame_list = []
    openMeteoFetcher = OpenMeteoFetcher()
    list_geohash_list = set()
    update_hours_interval = 3
    day = "08"
    month = "05"
    year = "2023"

    def __init__(self):
        config_file = open('config.json')
        config_parser = json.load(config_file)
        self.update_hours_interval = config_parser["granularityParameters"]["updateHoursInterval"]

    @staticmethod
    def add_is_day(dataframe):

        dataframe["is_day"] = 1

        # Define a condition
        condition = pandas.to_datetime(dataframe["time"]).dt.hour > 18

        # Update the selected positions with a new value
        dataframe.loc[condition, 'is_day'] = 0

        return dataframe

    def update_dataframe(self):

        for t, hashlist in enumerate(self.list_geohash_list):
            response = self.openMeteoFetcher.get_weather_forecast(hashlist, self.day, self.month, self.year)
            for i in range(len(self.list_geohash_list[t])):
                for parameter in response[i]['hourly']:
                    self.list_data_frame_list[t][i][str(parameter)] = response[i]['hourly'][str(parameter)]
                    self.list_data_frame_list[t][i] = self.add_is_day(self.list_data_frame_list[t][i])

    @staticmethod
    def fill_nan_values_with_mean(dataframe):
        return dataframe.fillna(method='ffill')

    def convert_dataframe_to_json(self, info):

        list_df_list = []

        for i, list_dataframe in enumerate(self.list_data_frame_list):
            df_list = {}
            for j, dataframe in enumerate(list_dataframe):
                dataframe = self.fill_nan_values_with_mean(dataframe)
                df_list[list(list(self.list_geohash_list)[i])[j]] = json.loads(dataframe.to_json())
            list_df_list.append(df_list)

        list_df_list.append(info)

        return list_df_list

    def waiter(self, input_queue, output_queue):

        while True:

            input_fetcher = InputParser()

            list_hash_list = input_queue.get()
            input_aoi = input_queue.get()

            self.day, self.month, self.year = input_fetcher.get_date(input_aoi)

            # I have already the resource requested
            if self.list_geohash_list == list_hash_list and self.list_data_frame_list:
                output_queue.put(self.convert_dataframe_to_json(input_aoi))
            # I have to request data to the api
            else:
                self.list_geohash_list = list_hash_list
                self.list_data_frame_list = []
                for i in range(len(self.list_geohash_list)):
                    self.list_data_frame_list.append([])
                    for j in range(len(self.list_geohash_list[i])):
                        self.list_data_frame_list[i].append(pandas.DataFrame())
                self.update_dataframe()
                output_queue.put(self.convert_dataframe_to_json(input_aoi))

    def updater(self):

        while True:

            if self.list_data_frame_list and self.list_geohash_list:
                self.update_dataframe()
            time.sleep(self.update_hours_interval * 60 * 60)
