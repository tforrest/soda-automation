import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

# set up app 
app = Flask(__name__)
# set up database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLASKDB']
db = SQLAlchemy(app)
# set up Twilio Variables 
app.config['TWILIO_ACCOUNT_SID'] = os.environ['TWILIO_ACCOUNT_SID']
app.config['TWILIO_AUTH_TOKEN'] = os.environ['TWILIO_AUTH_TOKEN']
app.config['TWILIO_NUM'] = os.environ["TWILIO_NUM"]
