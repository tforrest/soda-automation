from cerberus import Validator

from copy import deepcopy
from time import gmtime, strftime
import logging
import re

# schemas 
student_schema = {
    'fname': {
        'required': True, 
        'type':'string',
    },
    'last_name': {
        'required': True, 
        'type':'string',
    },
    'email_address': {
        'required': True, 
        'type':'string',
    },
    'number': {
        'type':'string',
    },
    'asuid': {
        'required': True, 
        'type':'string',
    },
    'class': { 
        'type':'string',
    }
}

bad_resp_match = lambda status: re.match(r"^[4,5][0-9][0-9]$",status)

v = Validator()

def validate_memmber(data):
    """Util function to validate incoming json"""
    if v.validate(data, student_schema):
        return (True,None)
    else:
        return (False,v.errors)


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
        if bad_resp_match(str(r.status_code)):
            logging.error("Failed to execute mailchimp command")
            logging.error(r.json())
        else:
            logging.info("Mailchimp operation success")
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

def transform_mailchimp_response(json_response):
    l = []
    for member in json_response['members']:
        data = dict()
        data["ID"] = member["id"]
        data["EMAIL"] = member["email_address"]
        
        # copy data in merge_fields
        temp = member["merge_fields"].copy()
        data.update(temp)
        l.append(data)
    return l
           

class FailedTransform(Exception):
    """Exception for Failed Mailchimp Transform"""
    def __init__(self,data="Not data"):
        self.error_string = 'Failed Transform: {}'
        Exception.__init__(self,self.error_string.format(data))     
    
class ChimpException(Exception):
    """Exception for Bad Response from MailChimp"""
    def __init__(self,error_string):
        Exception.__init__(self,error_string)
