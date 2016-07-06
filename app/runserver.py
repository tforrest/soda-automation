from flask_script import Manager

from config.config import app
# from mailchimp.redis_init import init_redis_with_mailchimp

manager = Manager(app)

@manager.command
def run_local():
    #init_redis_with_mailchimp(redis_server)
    app.run(debug=True)

@manager.command
def run_production():
    # TO-DO
    pass
    
if __name__ == '__main__':
    manager.run()
    