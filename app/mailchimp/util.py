from copy import deepcopy
from time import gmtime, strftime
import re

resp_match = lambda status: re.match(r"^[4,5][0-9][0-9]$",status)


mailchimp_shell_member = {
    "email_type": "html",
    "status": "subscribed",
    "merge_fields": {},
    "interests": "",
    "vip":"",
    "location": {},
    "ip_signup": "",
    "timestamp_signup": "",
    "timestamp_opt": "",
    "email_address": "",
}

def handle_chimp_response(func):
    """Utility function that pre processes a 
       mailchimp response
    """
    def wrapper(*args,**kwargs):
        r = func(*args,**kwargs)
        j = r.json()
        if resp_match(str(r.status_code)):
            raise ChimpException(j["status"],j["title"],j["detail"])
        return j
    return wrapper
  
def transform_member(func):
    """Ultility function that process a request to mailchimp schema""" 
    
    def wrapper(*args,**kwargs):
        if kwargs['data']:
            try:
                data = kwargs['data']
                processed = deepcopy(mailchimp_shell_member)
                processed['email'] =  data.pop('email')
                processed['merge_fields'].update(data)
                
                # set and return transformed data
                kwargs['data'] = processed
                return func(*args,**kwargs)
            except:
                raise FailedTransform(data)
        else:
            raise FailedTransform("No data")
         

class FailedTransform(Exception):
    """Exception for Failed Mailchimp Transform"""
    def __init__(self,data="Not data"):
        self.error_string = 'Failed Transform: {}'
        Exception.__init__(self,self.error_string.format(data))     
    
class ChimpException(Exception):
    """Exception for Bad Response from MailChimp"""
    def __init__(self,status,title,detail):
        self.error_string = 'Chimp Exception Status:{}, Title: {}, Detail: {}'
        Exception.__init__(self,self.error_string.format(status,title,detail))