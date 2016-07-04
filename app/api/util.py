from cerberus import Validator

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

resp_match = lambda status: re.match(r"^[4,5][0-9][0-9]$",status)

v = Validator()

def validate_memmber(data):
    """Util function to validate incoming json"""
    if v.validate(data, student_schema):
        return (True,None)
    else:
        return (False,v.errors)
        
    
    
   
        
    