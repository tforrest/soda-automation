from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
#from twilio_client import client

# config test app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


@app.route('/',methods=['GET','POST'])
def index():
    # message = client.messages.create(to="",from_="",
    # body="Test API")
    return message.body
    
if __name__ == '__main__':
    app.run(debug=True)