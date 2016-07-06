from flask_script import Manager
from config.config import app

manager = Manager(app)

# Deploy for development
@manager.command
def run_dev():
    app.run(debug=True)

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
    