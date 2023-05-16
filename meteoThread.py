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
        
        for x in response['hourly']:
            self.data_frame[str(x)] = response['hourly'][str(x)]

        self.data_frame['AOI_ID'] = id
        self.data_frame['EventID'] = id
        
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
