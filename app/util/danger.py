from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import request as flask_request
from flask import abort

import logging
import os

def gen_auth_token(id,expiration=10000):
    """Generate auth token"""
    try:
        s = Serializer(os.environ['API_KEY'],expires_in=expiration)
    except KeyError:
        logging.fatal("No API_KEY env")
        abort(500)

    return s.dumps({'id':id})

def verify_auth_token(token):
    """Verify auth token"""
    try:
        s = Serializer(os.environ['API_KEY'])
    except KeyError:
        logging.fatal("No API_KEY env")
        abort(500)
    # check the token and throw respective exception
    try:
        user = s.loads(token)
    except Exception as e:
        logging.warning("Bad token")
        abort(401)
    return user

def enable_auth(func):
    """Decorator to enable auth"""
    def wrapper(*args,**kwargs):
        re = flask_request
        # deny if not authorized
        if not re.headers.has_key("Authorization"):
            logging.warning("No token found")
            abort(401)
        auth = re.headers.get("Authorization").split(" ")
        # proces token 
        validate = verify_auth_token(auth[1])
        logging.debug("Valid auth! Yay")
        return func(*args,**kwargs)
    return wrapper