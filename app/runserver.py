from flask_script import Manager
from config.config import app

manager = Manager(app)

@manager.command
def run_local():
    app.run(debug=True)

@manager.command
def run_test():
    # To-Do
    pass

@manager.command
def run_production():
    # TO-DO
    pass
    
if __name__ == '__main__':
    manager.run()
    