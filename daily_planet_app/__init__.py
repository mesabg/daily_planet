from flask import Flask, render_template, request
from pymongo import *
from routes import create_routes
 
app = Flask(__name__, template_folder = 'templates', static_folder = 'static')

#Create Routes
create_routes(app)

# MongoDB Connection with PyMongo
def initDB ():
    client = MongoClient()
    db = client.daily_planet_db
    #db.create_collection("login")
    #db.create_collection("usuarios")
    #db.create_collection("articulos")
    return db

database = initDB()


if __name__ == '__main__':
	app.debug = True
	app.run()
