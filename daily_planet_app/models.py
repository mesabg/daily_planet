from pymongo import *

# MongoDB Connection with PyMongo
class Model:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.daily_planet_db
        self.db.create_collection("login")
        self.db.create_collection("usuarios")
        self.db.create_collection("articulos")