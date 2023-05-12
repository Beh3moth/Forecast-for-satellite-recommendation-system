import json


class Interface:
    def __init__(self):
        pass

    @staticmethod
    # Only method exposed to the other groups. It takes an aoi as input and returns the coordinates.
    # I have specified the type of the aoi and the return's type as str, but it could be different or omitted.
    # There could be also the need of some kind of check on the aoi (it could be empty ecc).
    # this method is static because it doesn't modify any instance or class attributes.
    def getWeatherForecast(aoi: str) -> str:
        # conversion in json?
        json_aoi = json.loads(aoi)

        # Check on the aoi?

        # Create the controller
        controller = Controller()

        # Call the method of the controller that takes the aoi as input and returns the final output.
        return controller.callTheProcessingMethod(json_aoi)


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def callTheProcessingMethod(json_aoi):
        # my code
        return json_aoi

































# import json
# import geopandas as gpd
#
# class Interface:
#     def __init__(self, controller):
#         self.controller = controller
#
#     def getJson(self, aoi):
#         weather_data = self.controller.get_weather_conditions(aoi)
#         if weather_data:
#             return json.dumps(weather_data, indent=4)
#         else:
#             return "Failed to retrieve weather data."

#     def getWeatherForecast(self, aoi):
#         forecast_data = self.controller.get_weather_forecast(aoi)
#         if forecast_data:
#             # Utilizza GeoPandas per creare un DataFrame geografico da forecast_data
#             # Assumiamo che forecast_data contenga le informazioni sulle geometrie
#             gdf = gpd.GeoDataFrame.from_features(forecast_data["features"])
#
#             # Salva il DataFrame geografico come file GeoJSON
#             output_file = "weather_forecast.geojson"
#             gdf.to_file(output_file, driver="GeoJSON")
#
#             return output_file
#         else:
#             return "Failed to retrieve weather forecast."
#
# #api_key = "YOUR_API_KEY"  # Inserisci qui la tua chiave API per il servizio meteo
# #controller = WeatherController(api_key)
# #interface = Interface(controller)
# #aoi = "40.7128,-74.0060"  # Esempio di AOI ( si può usare parametrica)
#
#
# # Ottieni le condizioni meteo come JSON
# #weather_json = interface.getJson(aoi)
# #print(weather_json)
#
# # Ottieni il forecast meteo come file GeoJSON
# #forecast_file = interface.getWeatherForecast(aoi)
# #print(f"Forecast saved as: {forecast_file}")
# */
#

