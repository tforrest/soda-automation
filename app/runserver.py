from flask_script import Manager
from flask_restful import Api
from config import app
from api import api

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
@manager.command
def run_dev():
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
    