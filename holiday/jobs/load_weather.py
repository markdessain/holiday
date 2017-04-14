import time

from settings import mongo, weather_api_key
from data.source import weather, locations


def run():
    areas = list(mongo.load(locations.Record))

    for location in areas:
        for record in weather.Source(weather_api_key, location.key(), location.coordinates).load():
            mongo.save(record)
            time.sleep(120) # Just to make sure we don't go over the daily limit


if __name__ == '__main__':
    run()
