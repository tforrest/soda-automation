from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

import os


# set up basic app 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLASKDB']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


