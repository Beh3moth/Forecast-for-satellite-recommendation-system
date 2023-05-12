import json
import geopandas as gpd

class Interface:
    def __init__(self, controller):
        self.controller = controller

    def getJson(self, aoi):
        weather_data = self.controller.get_weather_conditions(aoi)
        if weather_data:
            return json.dumps(weather_data, indent=4)
        else:
            return "Failed to retrieve weather data."

    def getWeatherForecast(self, aoi):
        forecast_data = self.controller.get_weather_forecast(aoi)
        if forecast_data:
            # Utilizza GeoPandas per creare un DataFrame geografico da forecast_data
            # Assumiamo che forecast_data contenga le informazioni sulle geometrie
            gdf = gpd.GeoDataFrame.from_features(forecast_data["features"])

            # Salva il DataFrame geografico come file GeoJSON
            output_file = "weather_forecast.geojson"
            gdf.to_file(output_file, driver="GeoJSON")

            return output_file
        else:
            return "Failed to retrieve weather forecast."
