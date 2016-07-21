from flask_restful import Resource, fields
from flask_restful import reqparse
from flask import request, abort, jsonify

from util.danger import gen_auth_token
from util.danger import enable_auth
from util.util import validate_memmber
from util.util import bad_resp_match

from mailchimp import chimp

from models.user import User
from models.redis_db import MailChimpRedis
from redis_ops.init_redis import RedisPopulater

import logging
import time
import base64
import json
import re

class MailChimpListCheck(Resource):
    """
    MailChimpListCheck lists the available mailchimp lists to query from 
    /api/lists/
    """
    method_decorators = [enable_auth]

    def __init__(self):
        super(Resource,self).__init__()
        self.redis_ops = RedisPopulater()
        
    def get(self):
        """
        GET the lists available to query
        """
        mailchimp_list_info = self.redis_ops.get_redis_info()

        if not mailchimp_list_info:

            return {"Not Data":"Redis empty! Check your config:)"},200

        return mailchimp_list_info, 202 


class MailChimpList(Resource):
    """
    MailChimpList endpoint adds member(s) to MailChimpList
    """
    method_decorators = [enable_auth]

    def __init__(self):
        super(Resource,self).__init__()
        self.redis_ops = RedisPopulater()

    def get(self,list_id,asu_id):
        """
        GET a member in redis or create pool of that id
        """

        mailchimp_list = self.redis_ops.get_list_db(list_id)

        if not mailchimp_list:
            return {"List Unavailable": "Mailchimp List {} not stored".format(list_id)}, 404
        
        member = mailchimp_list.redis_server.get(asu_id)

        if not member:
            return {"Member Status": False}, 200

        member = base64.b64decode(member)
        
        return {"member_status": True,"member_info":json.loads(member)}, 200

class GenerateAuthToken(Resource):
    """
    GenerateAuthToken endpoint creates a token if basic auth is accepted
    /api/gen_token/
    """
    def get(self):
        """
        GET a valid token if basic_auth is successful
        """
        auth = request.authorization

        self._check_basic_auth(auth)
        token = gen_auth_token(auth.username)
    
        resp = {
            "Success!": "Token created",
            "token": token,
        }
        return resp,201

    def _check_basic_auth(self,auth):
        """
        _check_basic_auth validates basic auth
        """
        if not auth:
            logging.info("Basic Auth not found")
            abort(400)
        u = auth.username
        db_user = User.query.filter_by(user_name=u).first()
        if not db_user:
            logging.info("User not found")
            abort(400)
        if not db_user.check_pass(auth.password):
            logging.info("Bad password!")
            abort(401)