import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


# set up app 
app = Flask(__name__)
# set up Api
api = Api(app)
# set up database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLASKDB']
db = SQLAlchemy(app)
