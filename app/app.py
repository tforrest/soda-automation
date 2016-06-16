from config import app
from messaging import text
from flask import make_response


@app.route('/',methods=['GET','POST'])
def index():
    T = text.TwilioTextWrapper("test",True)
    print "test"
    x = T.send_message("15005550006","test")
    return make_response(x.body)
if __name__ == '__main__':
    app.run(debug=True)