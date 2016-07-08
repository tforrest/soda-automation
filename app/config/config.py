from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os
from api import api





# set up app 
app = Flask(__name__)
# set up Api
service = Api(app)
service.add_resource(api.MailChimpList,'/api/list/<list_id>',endpoint='list')
service.add_resource(api.MailChimpMember,'/api/member/<asu_id>',endpoint='member')
service.add_resource(api.GenerateAuthToken,'/api/gen_token',endpoint='token')
# setup local basic redis server
# TO-DO more robust config process
# set up database
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLASKDB']
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
