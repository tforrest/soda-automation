from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadTimeSignature

import os

def gen_auth_token(id,expiration=10000):
    """Generate auth token"""
    s = Serializer(os.environ['API_KEY'],expires_in=expiration)
    return s.dumps({'id':id})

def verify_auth_token(token):
    """Verify auth token"""
    s = Serializer(os.environ['API_KEY'])
    
    # check the token and throw respective
    try:
        user = s.loads()
    except SignatureExpired:
        return False, "SignatureExpired bad token"
    except BadTimeSignature:
        return False, "BadSignature bad token"
    return True, user


    