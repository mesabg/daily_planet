from pymongo import *
from bson.son import SON

# MongoDB Connection with PyMongo
class Model:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.daily_planet_db
        
    def getSixFeed(self, inicio):
        save = list(self.db.articulos.aggregate([{ '$sort': {'fecha':1} },{'$project':{ '_id':1, 'imagen':1, 'nombre':1, 'cuerpo':1 }}]))
        array = []
        for i in range(inicio, inicio+6):
            if len(save) == i:
                break
            else:
                array += save[i]
        return array