import os
import redis
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from api import api
from redis.init_redis import init_redis_with_mailchimp



# set up app 
app = Flask(__name__)
# set up Api
service = Api(app)
service.add_resource(api.MailChimpList,'/list/<list_id>',endpoint='list')
service.add_resource(api.MailChimpMember,'/member/<asu_id>',endpoint='member')
# setup local basic redis server
# TO-DO more robust config process
# set up database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLASKDB']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
