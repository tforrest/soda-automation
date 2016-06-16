from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import os
# config test app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLASKDB']
app.config['TWILIO_ACCOUNT_SID'] = os.environ['TWILIO_ACCOUNT_SID']
app.config['TWILIO_AUTH_TOKEN'] = os.environ['TWILIO_AUTH_TOKEN']
app.config['TWILIO_NUM'] = "15005550006"
db = SQLAlchemy(app)
