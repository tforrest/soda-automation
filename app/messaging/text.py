from config import app
from twilio.rest import TwilioRestClient

class TwilioTextWrapper(object):
    
    def __init__(self,signature=None,debug=None):
        self._twilio_client = self._get_twilio_client()
        self._phone_number = app.config['TWILIO_NUM']
        self._signature = signature
        self.debug = debug
        
    def _get_twilio_client(self):
        
        try:
            twilio_account_sid =  app.config['TWILIO_ACCOUNT_SID']
            twilio_auth_token = app.config['TWILIO_AUTH_TOKEN']
            client = TwilioRestClient(twilio_account_sid ,twilio_auth_token )
            return client
        except:
            raise TwilioWrapperException("Failure to generate client")
    
    def send_message(self,to, message):
        
        m = self._twilio_client.messages.create(
            to=to,
            from_=self._phone_number,
            body=message,
        )
        return m
       
class TwilioWrapperException(Exception):
    pass