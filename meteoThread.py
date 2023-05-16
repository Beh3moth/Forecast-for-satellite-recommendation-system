import threading
import pandas as pd
from openMeteoFetcher import OpenMeteoFetcher
import time


class MeteoThread:

    data_frame = pd.DataFrame()
    openMeteoFetcher = OpenMeteoFetcher()
    geohash_list = set()

    def __init__(self):
        pass

    def run(self):

        # while True:

        id = 1
        # condition for updating the dataframe
        response = self.openMeteoFetcher.get_weather_forecast(self.geohash_list)[0]

        # self.data_frame['time'] = pd.to_datetime(response['hourly_units']['time']).strftime('%Y-%m-%dT%H:%M:%S')
        self.data_frame['time'] = response['hourly']['time']
        self.data_frame['AOI_ID'] = id
        self.data_frame['EventID'] = id
        self.data_frame['temperature'] = response['hourly']['temperature_2m']
        self.data_frame['precipitationProbability'] = response['hourly']['precipitation_probability']
        self.data_frame['cloudcover'] = response['hourly']['cloudcover']
        self.data_frame['day/night'] = response['hourly']['is_day']
        # time.sleep(3*60*60)

    def get_dataframe(self, geohash_list):

        # check if there are some geohash that are not in the geohash list
        self.geohash_list = geohash_list

        # start the thread
        meteo_thread = threading.Thread(self.run())

        if not meteo_thread.is_alive():
            meteo_thread.start()
            meteo_thread.join()

        return self.data_frame
