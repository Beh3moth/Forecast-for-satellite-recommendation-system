# Weather Forecast API
This project provides an API for retrieving weather forecasts based on specified parameters and geographic locations. The API utilizes data from the Open-Meteo service to provide accurate and up-to-date weather information.

## Project Structure
The project consists of several Python files:
- __init__.py: Start the Flask service and the API itself with two threads tha will run in parallel to answer to the request and to asynchronously update the forecasts.
- interface.py: Defines the interface class that acts as a bridge between the API and the weather forecast logic.
- meteoThread.py: Implements a thread for updating the weather forecast data in the background.
- geoHashConverter.py: Provides functionality for converting geographic coordinates to geohashes.
- controller.py: Defines the controller class that coordinates the processing of weather forecasts.
- input_parser.py: Implements the input parser class for parsing the API request payload.
- logger.py: Implements a logger class for logging API calls so that the maximum calls are not exceeded
- openMeteoFetcher.py: Fetches weather forecast data from the Open-Meteo service.

## API Endpoints
The API provides a single endpoint for retrieving weather forecasts:

POST /weatherforecast: Accepts a JSON payload specifying the geographic location and desired weather parameters. Returns the weather forecast for the specified location.

## How It Works
The API receives a POST request with a JSON payload containing the geographic location and desired weather parameters.
The Flask module in __init__.py  handles the request, parses the JSON payload, and passes the necessary data to the Interface class.
The Interface class, in turn, invokes the get_weather_forecast method to initiate the weather forecast processing.
The Controller class coordinates the processing by converting the given geographic location to a geohash, enqueuing it for further processing, and modifying the parameter list if necessary.
The MeteoThread class handles the background processing of weather forecasts by updating the data frames with weather information fetched from the Open-Meteo service.
The updated weather forecast data frames are converted to JSON format and returned as the API response.

## Dependencies
The project utilizes the following dependencies:

- Flask: A web framework for building the API.
- requests: A library for making HTTP requests to external services.
- geohash: A library for converting geographic coordinates to geohashes.
- shapely: A library for working with geometric objects.
- numpy: A library for numerical computations.
- pandas: A library for data manipulation and analysis.

## Configuration

The API has a configuration file (config.json) that can set some of the parameters of the application.