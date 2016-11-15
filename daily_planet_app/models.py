from pymongo import *

# MongoDB Connection with PyMongo
class Model:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.daily_planet_db