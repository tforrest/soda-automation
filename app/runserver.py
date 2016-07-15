from flask_script import Manager
from flask_restful import Api

from models.user import User
from redis_ops.init_redis import RedisService
from config import app
from config import db

from api import api

import logging
import os
import sys

manager = Manager(app)

def setup_api(app):
    """
    Config resources with flask app
    """
    service = Api(app)
    service.add_resource(api.MailChimpList,'/api/list/<list_id>',endpoint='list')
    service.add_resource(api.MailChimpMember,'/api/member/<asu_id>',endpoint='member')
    service.add_resource(api.GenerateAuthToken,'/api/gen_token',endpoint='token')

    return app

serviced_app = setup_api(app)

# Deploy for development
def setup_dev():
    """
    Setup dev environment 
    """

    # setup database for admin
    db.create_all()
    try:
        admin_user_name = os.environ['DEV_ADMIN_USER_NAME']
        admin_password = os.environ['DEV_ADMIN_PASSWORD']
    except KeyError as e:
        logging.warning(e)
        logging.fatal("Error cannot setup dev environment")
        sys.exit(2)

    admin = User(admin_user_name,admin_password)
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        logging.fatal(e)
        logging.fatal("Error cannot setup dev environment")
        sys.exit(2)

    # init redis and populate with mailchimp 
    r = RedisService()

    r.pull_mailchimp()

@manager.command
def run_dev():
    setup_dev()
    serviced_app.run(debug=True)

# Deploy for intergation tests
@manager.command
def run_test():
    # To-Do
    pass

# Deploy for production 
@manager.command
def run_production():
    # TO-DO
    pass
    
if __name__ == '__main__':
    manager.run()
    