from flask import Flask 
from twilio_client import client
# config test app
app = Flask(__name__)
<<<<<<< HEAD
<<<<<<< HEAD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/thomas/PersonalProjects/soda-twilio-service/test.db'
db = SQLAlchemy(app)
=======
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
>>>>>>> parent of 92d6afe... Add Flask-SQLAlchemy
=======
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
>>>>>>> parent of 92d6afe... Add Flask-SQLAlchemy


@app.route('/',methods=['GET','POST'])
def index():
    message = client.messages.create(to="",from_="",
    body="Test API")
    return message.body
    
if __name__ == '__main__':
    app.run(debug=True)