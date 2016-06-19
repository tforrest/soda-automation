import re

resp_match = lambda status: re.match(r"^[4,5][0-9][0-9]$",status)

def handle_chimp_response(func):
    """Utility function that pre processes a 
       mailchimp response
    """
    def wrapper(*args,**kwargs):
        r = func(*args,**kwargs)
        if resp_match(str(r["status"])):
            raise ChimpException(r["status"],r["title"],r["detail"])
        return r
    return wrapper
    
    
class ChimpException(Exception):
    """Exception for Bad Response from MailChimp"""
    def __init__(self,status,title,detail):
        self.error_string = 'Chimp Exception Status:{}, Title: {}, Detail: {}'
        Exception.__init__(self,self.error_string.format(status,title,detail))