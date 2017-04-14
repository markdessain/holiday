import time
import requests

from . import Source
from .. import Record


class Source(Source):

    def __init__(self, client_id, access_token, location):
        self.client_id = client_id
        self.access_token = access_token
        self.location = location

    def load(self):

        limit = 50

        for i in range(6):
            offset = i * limit

            payload = {
                'client_id': self.client_id,
                # 'locale': 'en-US',
                'currency': 'GBP',
                '_format': 'for_search_results',
                '_limit': limit,
                '_offset': offset,
                'fetch_facets': False,
                # 'guests': 1,
                'location': self.location,
                # 'min_bathrooms': 0,
                # 'min_bedrooms': 0,
                # 'min_beds': 1
            }

            r = requests.get("https://api.airbnb.com/v2/search_results", params=payload)

            for result in r.json()['search_results']:
                result['location'] = {
                  'type' : 'Point',
                  'coordinates' : [result['listing']['lng'], result['listing']['lat']]
                }
                yield Record(result)

            time.sleep(5) # Lets not hammer airbnb too much


class Record(Record):

    @property
    def id(self):
        return self.json['listing']['id']

    @property
    def name(self):
        return self.json['listing']['name']

    @property
    def city(self):
        return self.json['listing']['city']

    @property
    def reviews_count(self):
        return self.json['listing']['reviews_count']

    @property
    def star_rating(self):
        return self.json['listing']['star_rating']

    @property
    def property_type(self):
        return self.json['listing']['property_type']

    @property
    def room_type(self):
        return self.json['listing']['room_type']

    @property
    def lng(self):
        return self.json['listing']['lng']

    @property
    def lat(self):
        return self.json['listing']['lat']

    @property
    def nightly_price(self):
        return self.json['pricing_quote']['nightly_price']
