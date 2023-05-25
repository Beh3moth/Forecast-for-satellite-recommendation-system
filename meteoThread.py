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

    # Update the data frames with weather forecast information.
    def update_dataframe(self):

        for t, hashlist in enumerate(self.list_geohash_list):
            response_list = self.openMeteoFetcher.get_weather_forecast(hashlist, self.day, self.month, self.year)
            for i, response in enumerate(response_list):
                self.list_data_frame_list[t][i] = response

    # Fill NaN values in the DataFrame with the mean of the previous values.
    @staticmethod
    def fill_nan_values_with_mean(dataframe):
        return dataframe.fillna(method='ffill')

    # Convert the data frames to JSON format so that it can be returned as output of the POST request.
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

    # Re-initialize the list of lists of dataframe with Null values so that it can be filled later.
    def re_initialize_dataframes(self, list_hash_list):

        self.list_geohash_list = list_hash_list
        self.list_data_frame_list = []

        for i in range(len(self.list_geohash_list)):
            self.list_data_frame_list.append([])
            for j in range(len(self.list_geohash_list[i])):
                self.list_data_frame_list[i].append(pandas.DataFrame())

    # Function used as thread number 1 that has to wait for input from the input_queue and process it.
    def waiter(self, input_queue, output_queue):

        while True:

            input_fetcher = InputParser()

            list_hash_list = input_queue.get()
            input_aoi = input_queue.get()

            self.day, self.month, self.year = input_fetcher.get_date(input_aoi)

            # Case in which there is already the dataframe requested.
            # It is the case in which the hashlist requested is the same of the hashlist saved and the
            # list of lists of dataframe is not empty.
            if self.list_geohash_list == list_hash_list and self.list_data_frame_list:
                output_queue.put(self.convert_dataframe_to_json(input_aoi))
            # Case in which I have to ask data to the api to initialize the dataframes.
            else:
                self.re_initialize_dataframes(list_hash_list)
                self.update_dataframe()
                output_queue.put(self.convert_dataframe_to_json(input_aoi))

    # Function used as thread number 2 that has to periodically update the data frames. The update interval is
    # an attribute of the class.
    def updater(self):

        while True:

            if self.list_data_frame_list and self.list_geohash_list:
                self.update_dataframe()
            time.sleep(self.update_hours_interval * 60 * 60)
