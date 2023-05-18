import threading
import queue
from interface import Interface
import json
from flask import Flask
from flask import request
import time
from meteoThread import MeteoThread

app = Flask(__name__)

with open('AOIs\#0001_AoiID_1.geojson') as f:
    data = json.load(f)

interface = Interface()
# Create a shared message queue
input_queue = queue.Queue()
output_queue = queue.Queue()


@app.route('/', methods=['POST'])
def upload_file():
    try:
        file = request.get_json()
        interface.get_weather_forecast(file, input_queue)
        print("siamo tornati sul test!")
        output = output_queue.get()
        print("output da test")
        return output
    except json.JSONDecodeError:
        return 'Invalid JSON file.', 400


meteoThread = MeteoThread()

thread = threading.Thread(target=meteoThread.get_dataframe_thread, args=(input_queue, output_queue))
thread.start()


