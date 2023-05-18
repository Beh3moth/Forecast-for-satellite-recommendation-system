import threading
import queue
from interface import Interface
import json
from flask import Flask
from flask import request
from meteoThread import MeteoThread

app = Flask(__name__)

interface = Interface()

# Create a shared message queue
input_queue = queue.Queue()
output_queue = queue.Queue()


def add_event_info(json_file):
    info = {}
    info["eventId"] = json_file["features"][0]["properties"]["eventId"]
    info["eventType"] = json_file["features"][0]["properties"]["eventType"]
    info["lat"] = json_file["features"][0]["properties"]["lat"]
    info["long"] = json_file["features"][0]["properties"]["long"]
    return info


@app.route('/', methods=['POST'])
def upload_file():
    try:
        file = request.get_json()
        interface.get_weather_forecast(file, input_queue)
        output = output_queue.get()
        info = add_event_info(file)
        output.append(info)
        return str(json.dumps(output))
    except json.JSONDecodeError:
        return 'Invalid JSON file.', 400


meteoThread = MeteoThread()

# Create two threads, each executing a different function of the class
waiter = threading.Thread(target=meteoThread.waiter, args=(input_queue, output_queue))
updater = threading.Thread(target=meteoThread.updater)

# Start the threads
waiter.start()
updater.start()
