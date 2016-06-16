from app import app
from twilio import TwilioRestClient

class TwilioTextWrapper(object):
    
    def __init__(self,signature,debug):
        self._twilio_client = _get_twilio_client()
        self._twilio_number = app.config['TWILIO_NUMBER']
        self._signature = signature
        self.debug = debug
        
    def _get_twilio_client(self):
        
        try:
            twilio_account_sid =  app.config['TWILIO_ACCOUNT_SID']
            twilio_auth_token = app.config['TWILIO_AUTH_TOKEN']
            client = TwilioRestClient(account_sid,auth_token)
            return client
        except:
            raise TwilioWrapperException("Failure to generate client")
    
    def send_single_message(self,to,from,message):
        
        message = self._twilio_client.messages.create(
            to=to,
            from_=from,
            body=message,
        )
        
        return _hand_twilio_text_respose(message.response)
        
    def send_messages(self,from,message,recipients):
        
        for recipient in recipients:
            message = self._twilio_client.messages.create(
                to=recipient.to
                from_=from,
                body = message
            )
            if not self._handl_twilio_text_response(message.response):
                return False
       return True
        
    def _handle_twilio_text_response(self,response):
        return True 

class TwilioWrapperException(Exception):
    pass