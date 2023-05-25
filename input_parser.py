
class InputParser:

    @staticmethod
    def get_date(input_aoi):
        input_aoi["date"] = input_aoi["features"][0]["properties"]["date"]
        date = str(input_aoi["date"]).split(" ")[0]
        day = date.split('-')[2]
        month = date.split('-')[1]
        year = date.split('-')[0]
        return day, month, year
