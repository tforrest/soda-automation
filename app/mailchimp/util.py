import re

resp_match = lambda status: re.match(r"^[4,5][0-9][0-9]$",status)

def handle_response(func):
    """Utility function that pre processes a 
       mailchimp response
    """
    r = func()
    try:
        if resp_match(r["status"]):
           raise ChimpException(r["status"],r["title"],r["detail"])
    except:
        raise ChimpException("404","Not Found","Status not found")
    
    return response
    
class ChimpException(Exception):
    """Exception for Bad Response from MailChimp"""
    error_string = 'Chimp Exception Status:{}, Title: {}, Detail: {}'
    def __init__(self,status,title,reason):
        Exception.__init__(self,error_string.format(status,title,detail))