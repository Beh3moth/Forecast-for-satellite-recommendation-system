import requests
from apiFetcher import ApiFetcher
import geohash
import threading


class OpenMeteoFetcher(ApiFetcher):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        def get_weather_forecast(self, geohash_list):
            response_list = []

            for el in geohash_list:
                lat, lon = geohash.decode(el)
                base_url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=9.19" + str(
                    lon) + "&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature," \
                           "precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,weathercode," \
                           "pressure_msl,surface_pressure,cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high," \
                           "visibility,evapotranspiration,et0_fao_evapotranspiration,vapor_pressure_deficit," \
                           "windspeed_10m,windspeed_80m,windspeed_120m,windspeed_180m,winddirection_10m," \
                           "winddirection_80m,winddirection_120m,winddirection_180m,windgusts_10m,temperature_80m," \
                           "temperature_120m,temperature_180m,soil_temperature_0cm,soil_temperature_6cm," \
                           "soil_temperature_18cm,soil_temperature_54cm,soil_moisture_0_1cm,soil_moisture_1_3cm," \
                           "soil_moisture_3_9cm,soil_moisture_9_27cm,soil_moisture_27_81cm,is_day"
                response = requests.get(base_url)
                response = response.json()
                response_list.append(response)

            return response_list