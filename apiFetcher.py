from abc import ABC, abstractmethod


class ApiFetcher(ABC):
    @abstractmethod
    def get_weather_forecast(self, geohash_list: set):
        pass

    # @abstractmethod
    # def get_weather_forecast(self, lat, lon):
    #     pass