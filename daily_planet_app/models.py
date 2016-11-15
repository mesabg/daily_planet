from pymongo import *

# MongoDB Connection with PyMongo
class Model:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.daily_planet_db
        #db.create_collection("login")
        #db.create_collection("usuarios")
        #db.create_collection("articulos")