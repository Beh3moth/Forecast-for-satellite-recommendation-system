import threading
import queue
from interface import Interface
from shapely import Polygon

lat_point_list = [50.854457, 50.924457, 52.518172, 50.072651, 48.853033]
lon_point_list = [4.377184, 4.377184, 13.407759, 14.435935, 2.349553]

polygon_geom = Polygon(zip(lon_point_list, lat_point_list))

# Create a shared message queue
message_queue = queue.Queue()

interface = Interface()
thread = threading.Thread(target=interface.get_weather_forecast, args=(polygon_geom, message_queue,))
thread.start()


def getForecast():
    print(message_queue.get())


getForecast()
getForecast()