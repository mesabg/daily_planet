from pymongo import *

# MongoDB Connection with PyMongo
class Model:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.daily_planet_db
        
    def getSixFeed(inicio):
        save = self.db.articulos.aggregate([{ $sort: {"fecha":1} },{$project:{ _id:1, imagen:1, nombre:1, cuerpo:1 }}]).toArray()
        array = []
        for i in range(inicio, inicio+6):
            if save.length == i:
                break
            else
                array += save[i]
            
        return array