import logging
from multiprocessing import Pool

from settings import mongo, airbnb_api_key
from data.source import airbnb_listing, locations
from data.derived import airbnb_zones

log = logging.getLogger(__name__)


def run():
    areas = list(mongo.load(locations.Record))

    p = Pool(8)
    # p.map(load, areas)
    p.map(zones, areas)


def load(location):
    log.info('Starting: %s' % location)
    for record in airbnb_listing.Source(airbnb_api_key, None, location.name).load():
        mongo.save(record)
    log.info('Finished: %s' % location)


def zones(location):
    record = airbnb_zones.Query(mongo, location.key(), location.coordinates).run()
    mongo.save(record)


if __name__ == '__main__':
    run()
