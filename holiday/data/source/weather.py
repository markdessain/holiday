import time
import calendar

import requests

from . import Source
from .. import Record


class Source(Source):

    def __init__(self, api_key, name, coordinates):
        self.api_key = api_key
        self.name = name
        self.coordinates = coordinates

    def load(self):

        months = {}

        for month in range(1, 13):
            first_day = str(month).zfill(2) + '01'
            last_day = str(month).zfill(2) + str(calendar.monthrange(2002, month)[1]).zfill(2)

            r = requests.get(
                'http://api.wunderground.com/api/{api_key}/planner_{first_day}{last_day}/q/{coordinates}.json'.format(
                    api_key=self.api_key,
                    first_day=first_day,
                    last_day=last_day,
                    coordinates=','.join(map(str, self.coordinates))
                )
            )
            months[calendar.month_name[month]] = r.json()['trip']

            time.sleep(5) # Lets not hammer weather too much. They have a strict policy

        yield Record({
            'location': self.name,
            'months': months
        })


class Record(Record):

    @property
    def id(self):
        return self.json['location']
