from flask import Flask, render_template, request
from routes import create_routes
from models import *

#Create Flask Application
app = Flask(__name__, template_folder = 'templates', static_folder = 'static')

#Create Database
model = Model();

#Create Routes
create_routes(app, model)

if __name__ == '__main__':
	app.debug = True
	app.run()
