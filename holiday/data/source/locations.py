from geopy.geocoders import Nominatim

from . import Source
from .. import Record


class Source(Source):

    def load(self):

        areas = {
            'Europe': {
                'UK': {
                    'Greater London': [
                        'London',
                        'Stratford',
                        'Isle of Dogs',
                        'Edgware',
                        'Watford',
                        'Romford',
                        'Dartford',
                        'Croydon',
                        'Twickenham',
                        'Hayes',
                        'Cheshunt',
                        'Twickenham',
                    ],
                    'Yorkshire': [
                        'York',
                        'Harrogate',
                        'Knaresborough',
                        'Leeds',
                        'Sheffield',
                        'Doncaster'
                    ]
                }
            }
        }

        geolocator = Nominatim()

        for continent, countries in areas.items():
            for country, regions in countries.items():
                for region, cities in regions.items():
                    for city in cities:
                        name = ','.join([city, region, country])
                        x = geolocator.geocode(name)
                        yield Record({
                            'continent': continent,
                            'country': country,
                            'city': city,
                            'region': region,
                            'name': name,
                            'longitude': x.longitude,
                            'latitude': x.latitude
                        })


class Record(Record):

    @property
    def id(self):
        return self.json['name']

    @property
    def name(self):
        return self.json['name']

    @property
    def continent(self):
        return self.json['continent']

    @property
    def country(self):
        return self.json['country']

    @property
    def region(self):
        return self.json['region']

    @property
    def city(self):
        return self.json['city']

    @property
    def coordinates(self):
        return self.json['latitude'], self.json['longitude']
