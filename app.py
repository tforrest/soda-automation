from flask import Flask 
from twilio_client import client
# config test app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'


@app.route('/',methods=['GET','POST'])
def index():
    message = client.messages.create(to="4807603293",from_="+15005550006",
    body="Test API")
    return message.body
    
if __name__ == '__main__':
    app.run(debug=True)