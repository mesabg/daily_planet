from pymongo import *
from bson.son import SON
import datetime

# MongoDB Connection with PyMongo
# https://docs.mongodb.com/manual/reference/operator/query/regex/
class Model:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.daily_planet_db
        self.termine = False
        
    def getSixFeedPub(self,inicio,tipo,busqueda):
        if tipo == "Fecha":
            save = list(self.db.articulos.aggregate([{ '$sort': {'fecha':1} },{'$project':{ '_id':1, 'imagen':1, 'nombre':1, 'resumen':1,'publicado':1 }}]))
        else:
            save = list(self.db.articulos.aggregate([{ '$sort': {'nombre':1} },{'$project':{ '_id':1, 'imagen':1, 'nombre':1, 'resumen':1,'publicado':1 }}]))
        array = list() 
        
        
        if busqueda != "": 
            busqueda = busqueda.lower()
            for lista in save:
                if busqueda not in lista['nombre'].lower():
                    continue
                elif lista['publicado']:
                    array.append(lista)
        else:
            for i in range(inicio, inicio+6):
                if len(save) == i:
                    break
                else:
                    if save[i]['publicado']:
                        array.append(save[i])
        return array
        
        
    def getSixFeedNoPub(self,inicio):
        save = list(self.db.articulos.aggregate([{ '$sort': {'fecha':1} },{'$project':{ '_id':1, 'imagen':1, 'nombre':1, 'resumen':1, 'publicado':1,'editando':1,'fecha':1,'cuerpo':1,'palabras':1 }}]))
        array = list() 
        
        for lista in save:
            if not lista['publicado']:
                variable = {'nombre':lista['nombre'],'fecha':str(lista['fecha']),'editando':lista['editando'],'publicado':lista['publicado'],'_id':lista['_id'],'imagen':lista['imagen'],'cuerpo':lista['cuerpo'],'palabras':lista['palabras'],'resumen':lista['resumen']}
                array.append(variable)
        return array
        
        
    def getSixFeed(self, inicio):
        save = list(self.db.articulos.aggregate([{ '$sort': {'fecha':1} },{'$project':{ '_id':1, 'imagen':1, 'nombre':1, 'resumen':1,'publicado':1 }}]))
        array = list() 
        
        for i in range(inicio, inicio+6):
            if len(save) == i:
                break
            else:
                if save[i]['publicado']:
                    array.append(save[i])
        return array
        
    def getSingle(self, _id_):
        return self.db.articulos.aggregate([ {'$match': {'_id': {'$eq':_id_}}} ,{ '$project':{'_id':1, 'autor':1, 'fecha':1, 'comentarios':1, 'nombre':1, 'cuerpo':1, 'categoria':1, 'imagen':1} }, {'$lookup':{ 'from':'usuarios', 'localField':'autor', 'foreignField':'_id', 'as':'autor_' }},  {'$project':{'_id':1, 'autor':'$autor_.nombre', 'fecha':1, 'comentarios':1, 'nombre':1, 'cuerpo':1, 'categoria':1, 'imagen':1  }}, { '$unwind': '$autor' } ])
        #return self.db.articulos.find_one({'_id':{'$eq':_id_}})
        #db.articulos.aggregate([ {'$match': {'_id': {'$eq':1}}} ,{ '$project':{'autor':1, 'fecha':1, 'comentarios':1, 'nombre':1, 'cuerpo':1, 'categoria':1} }, {'$lookup':{ 'from':'usuarios', 'localField':'autor', 'foreignField':'_id', 'as':'autor_' }},  {'$project':{'autor':'$autor_.nombre', 'fecha':1, 'comentarios':1, 'nombre':1, 'cuerpo':1, 'categoria':1  }} ])
        
    
    def get_image_username(self,name):
        data = self.db.usuarios.find_one({'nombre':{'$eq':name}},{'_id':0,'avatar':1})
        return data['avatar']
        
    def upload_comentario(self,id_articulo,id_usuario,comentario):
        nombre = self.db.usuarios.find_one({'_id':{'$eq':id_usuario}})['nombre']
        _idcomment = int (self.db.articulos.find_one({'_id':{'$eq':id_articulo}})['n_comment']) + 1
        self.db.articulos.update({'_id':id_articulo},{ '$inc': { 'n_comment': _idcomment }})
        data = {'_id':_idcomment,'nombre':nombre,'cuerpo':comentario,'fecha':str(datetime.datetime.now()),'respuestas':[] }
        data_ = {'_id':_idcomment,'nombre':nombre,'cuerpo':comentario,'fecha':datetime.datetime.now(),'respuestas':[] }
        self.db.articulos.update({'_id':id_articulo},{'$push':{'comentarios':data_}})
        return data
        
    def login(self,correo,password):
        return self.db.usuarios.find_one({'correo':{'$eq':correo},'password':{'$eq':password}})
        
    def registro(self,nombre,email,password,tipo):
        respuesta = self.db.usuarios.find_one({'correo':{'$eq':email}})
        respuesta2 = self.db.usuarios.find_one({'nombre':{'$eq':nombre}})
        
        if not respuesta and not respuesta2:
            id_all = self.db.usuarios.aggregate([{'$sort':{'_id':-1}},{'$limit':1}])
            _id_ = None
            for elem in id_all:
                _id_ = elem
            id_number = _id_['_id'] + 1
            self.db.usuarios.insert_one({'_id':id_number,'correo':email,'password':password, 'tipo': tipo, 'nombre': nombre, 'avatar': "local_images/user/1.png", 'descripcion': "vacio"})
            return True
        else:
            return False
        
    def publicar(self,_id,editor):
        editores = self.db.articulos.find_one({'_id':_id},{'_id':0,'editor':1})
        if not editor in editores['editor']:
            self.db.articulos.update({'_id':_id},{'$push':{'editor':editor}})
        self.db.articulos.update({'_id':_id},{'$set':{'publicado':True}})
        return True
    
    def modificar(self,_id,nombre,resumen,palabras,image,cuerpo,editor):
        editores = self.db.articulos.find_one({'_id':_id},{'_id':0,'editor':1})
        if not editor in editores['editor']:
            self.db.articulos.update({'_id':_id},{'$push':{'editor':editor}})
        self.db.articulos.update({'_id':_id},{'$set':{'nombre':nombre,'resumen':resumen,'palabras':palabras,'imagen':image,'cuerpo':cuerpo}})
        return
    
    def modificar_no_image(self,_id,nombre,resumen,palabras,cuerpo,editor):
        editores = self.db.articulos.find_one({'_id':_id},{'_id':0,'editor':1})
        if not editor in editores['editor']:
            self.db.articulos.update({'_id':_id},{'$push':{'editor':editor}})
        self.db.articulos.update({'_id':_id},{'$set':{'nombre':nombre,'resumen':resumen,'palabras':palabras,'cuerpo':cuerpo}})
        return
    
    def crear(self,nombre,resumen,palabras,image,cuerpo,autor):
        id_all = self.db.articulos.aggregate([{'$sort':{'_id':-1}},{'$limit':1}])
        _id_ = None
        for elem in id_all:
            _id_ = elem
        id_number = _id_['_id'] + 1
        self.db.articulos.insert_one({'_id':id_number,'nombre':nombre,'resumen':resumen,'palabras':palabras,'imagen':image,'cuerpo':cuerpo,'autor':autor,'editor':[],'comentarios':[],'categoria':'Noticias','fecha':datetime.datetime.now(),'editando':'No','publicado':False,'favoritos':[]})
        return
    
    def get_user_data (self, _id):
        return self.db.usuarios.find_one({'_id':_id})
        
        
    def addfav(self,_id_art,_id):
        array = self.db.articulos.find_one({'_id':int(float(_id_art))})['favoritos']
        if _id in array:
            return False
        else:
            self.db.articulos.update({'_id':_id_art},{'$push':{'favoritos':_id}})
            return True
    
    def upload_comentario_recursive(self,id_articulo, id_usuario,id_padre, text):
        def search_recursive(comentarios, _id):
            for comentario in comentarios:
                if self.termine:
                    return []
                if comentario['_id'] == _id:
                    self.termine = True
                    return [ comentario['_id'] ]
                else:
                    return [ comentario['_id'] ] + search_recursive(comentario['respuestas'], _id)
        resp = self.db.articulos.find_one({'_id':id_articulo},{'comentarios':1})
        array = search_recursive(resp,id_padre)
        
        self.termine = False
        print(array)
                    
       # [ 1, 4, 6, 8, 12 ]
       # self.db.articulos.update({'_id':id_articulo},{'$push':{'comentarios':data_}})
            
       # resp = self.db.articulos.find_one({'_id':id_articulo},{'comentarios':1})
        
       # nombre = self.db.usuarios.find_one({'_id':{'$eq':id_usuario}})['nombre']
    #    _idcomment = int (self.db.articulos.find_one({'_id':{'$eq':id_articulo}})['n_comment']) + 1
     #   self.db.articulos.update({'_id':id_articulo},{ '$inc': { 'n_comment': _idcomment }})
        
      #  data = {'_id':_idcomment,'nombre':nombre,'cuerpo':comentario,'fecha':str(datetime.datetime.now()),'respuestas':[] }
       # data_ = {'_id':_idcomment,'nombre':nombre,'cuerpo':comentario,'fecha':datetime.datetime.now(),'respuestas':[] }
    #    self.db.articulos.update({'_id':id_articulo},{'$push':{'comentarios':data_}})
        return data
    
    
    
    
    
    
    
    
    
    
    
    
        