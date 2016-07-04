from copy import deepcopy
import logging
from time import gmtime, strftime
import re

resp_match = lambda status: re.match(r"^[4,5][0-9][0-9]$",status)


mailchimp_shell_member = {
    "email_type": "html",
    "status": "subscribed",
    "merge_fields": {},
    "location": {},
    "ip_signup": "",
    "timestamp_signup": "",
    "timestamp_opt": "",
    "email_address": "",
}

def handle_chimp_response(func):
    """Utility function that loggs the error
    """
    def wrapper(*args,**kwargs):
        r = func(*args,**kwargs)
        if resp_match(str(r.status_code)):
            logging.error("Failed to execute mailchimp command")
            logging.error(r.json())
        return r
    return wrapper
  
def transform_member(func):
    """Utility function that process a request to mailchimp schema""" 
    
    def wrapper(*args,**kwargs):
        data = args[2]
        processed = deepcopy(mailchimp_shell_member)
        processed['email_address'] =  data.pop('email_address')
        processed['merge_fields'].update(data)

        # set and return transformed data
        return func(args[0],args[1],processed)
    return wrapper
           

class FailedTransform(Exception):
    """Exception for Failed Mailchimp Transform"""
    def __init__(self,data="Not data"):
        self.error_string = 'Failed Transform: {}'
        Exception.__init__(self,self.error_string.format(data))     
    
class ChimpException(Exception):
    """Exception for Bad Response from MailChimp"""
    def __init__(self,error_string):
        Exception.__init__(self,error_string)
