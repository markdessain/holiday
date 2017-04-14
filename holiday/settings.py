import logging
from data.mongo import MongoDb

logging.basicConfig(level=logging.DEBUG)

mongo = MongoDb('holiday')


weather_api_key = 'xxxx'
airbnb_api_key = 'xxxx'
