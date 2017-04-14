from settings import mongo
from data.source import locations



def run():
    for record in locations.Source().load():
        mongo.save(record)


if __name__ == '__main__':
    run()
