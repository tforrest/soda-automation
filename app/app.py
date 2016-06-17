from config import app
from config import db
from messaging import text

@app.route('/',methods=['GET','POST'])
def index():
    Tw =  text.TwilioTextWrapper()
    m = Tw.send_message("123","Test")
    return m
    
if __name__ == '__main__':
    app.run(debug=True)