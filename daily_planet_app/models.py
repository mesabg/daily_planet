from pymongo import *
from bson.son import SON

# MongoDB Connection with PyMongo
class Model:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.daily_planet_db
        
    def getSixFeed(self, inicio):
        save = list(self.db.articulos.aggregate([{ '$sort': {'fecha':1} },{'$project':{ '_id':1, 'imagen':1, 'nombre':1, 'resumen':1 }}]))
        array = list() 
        
        for i in range(inicio, inicio+6):
            if len(save) == i:
                break
            else:
                array.append(save[i])
        return array
        
    def getSingle(self, _id_):
        save = self.db.articulos.find_one({'_id':{'$eq':'1'}})
        print(save)
        return save
        
        # REVISAR RICARDO 