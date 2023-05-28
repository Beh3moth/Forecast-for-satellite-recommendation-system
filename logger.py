import json
import datetime


class Logger:

    @staticmethod
    def add_call():
        # Read the JSON file
        data = json.load(open("Memory/calls_log.json"))

        # Get the current date
        current_date = datetime.date.today().strftime('%Y-%m-%d')

        # Check if the date needs to be reset
        if data.get('date') != current_date:
            data['date'] = current_date
            data['counter'] = 0

        # Increment the counter
        data['counter'] += 1

        # Update the JSON file
        with open("Memory/calls_log.json", 'w') as file:
            json.dump(data, file)
