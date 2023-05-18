import threading
import queue
from interface import Interface

import json

from flask import Flask
from flask import request
import time

app = Flask(__name__)

with open('AOIs\#0001_AoiID_1.geojson') as f:
    data = json.load(f)

@app.route('/', methods=['POST'])
def upload_file():
    try:
        file = data
        return file
    except json.JSONDecodeError:
        return 'Invalid JSON file.', 400


# Create a shared message queue
message_queue = queue.Queue()

interface = Interface()

thread = threading.Thread(target=interface.get_weather_forecast, args=(upload_file(), message_queue,))
thread.start()


def get_forecast():
    print(message_queue.get())
    time.sleep(10)
    print(message_queue.get())
    thread.join()


get_forecast()
