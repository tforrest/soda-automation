import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from api import api as a

# set up app 
app = Flask(__name__)
# set up Api
api = Api(app)
api.add_resource(a.MailChimpApi,'/<list_id>')
# set up database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLASKDB']
db = SQLAlchemy(app)

# set up Twilio Variables 
# app.config['TWILIO_ACCOUNT_SID'] = os.environ['TWILIO_ACCOUNT_SID']
# app.config['TWILIO_AUTH_TOKEN'] = os.environ['TWILIO_AUTH_TOKEN']
# app.config['TWILIO_NUM'] = os.environ["TWILIO_NUM"]
# app.config['MAILCHIMP_USER'] = os.environ['MAILCHIMP_USER']
# app.config['MAILCHIMP_AUTH'] = os.environ['MAILCHIMP_AUTH']
