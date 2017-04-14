from collections import defaultdict

from . import Query
from .. import Record
from ..source import airbnb_listing


class Query(Query):

    def __init__(self, db, name, coordinates):
        super().__init__(db)
        self.name = name
        self.coordinates = coordinates

    def run(self):

        zone_distances = [0, 1000, 2000, 5000, 10000]

        values = {}

        for i in range(len(zone_distances)-1):
            room_types = defaultdict(list)

            for record in self.db.load(
                airbnb_listing.Record,
                {
                    'location': {
                        '$near': {
                            '$geometry': {
                                'type': "Point" ,
                                'coordinates': [self.coordinates[1], self.coordinates[0]] # Mongo stores lng, lat
                            },
                            '$minDistance': zone_distances[i],
                            '$maxDistance': zone_distances[i+1]
                        }
                    }
                },
                {
                    '_id': 0,
                    'pricing_quote.nightly_price': 1,
                    'listing.room_type': 1,
                }
            ):
                room_types[record.room_type].append(record.nightly_price)

            totals = {}

            for room_type, prices in room_types.items():
                if len(prices):
                    totals[room_type] = sum(prices)/len(prices)

            values[str(zone_distances[i+1])] = totals

        return Record(
            {
                'location': self.name,
                'prices': values
            }
        )


class Record(Record):

    @property
    def id(self):
        return self.json['location']

    @property
    def prices(self):
        return self.json['prices']
