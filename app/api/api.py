from flask_restful import Resource, fields
from flask_restful import reqparse
from flask import request, abort

from util.danger import gen_auth_token
from util.danger import enable_auth
from util.util import validate_memmber
from util.util import bad_resp_match

from mailchimp import chimp

from models.user import User
from redis_ops.init_redis import RedisService

import logging

class MailChimpList(Resource):
    """
    MailChimpList endpoint adds member(s) to MailChimpList
    """
    method_decorators = [enable_auth]
    def __init__(self):
        super(Resource,self).__init__()
        self.requester = chimp.ChimpRequester()

    def post(self,list_id):
        """
        Add a member(s) to a list
        """
        data = request.get_json()
        # check if valid request
        v = validate_memmber(data)
        if not v[0]:
            return v[1], 400
        result = self.requester.add_member(list_id,data)
        if not result:
            return {"Errors" : {
                "MailChimp":"Failure to insert member",
            }}, 418
        return r.json(),r.status_code

class MailChimpMember(Resource):
    """
    MailChimpMember endpoint checks if someone is part of a list 
    """
    method_decorators = [enable_auth]
    def __init__(self):
        super(Resource,self).__init__()
        self.redis_service = RedisService()

    def get(self,asu_id):
        """
        GET to see if a member is part of a <list>
        """
        member = self._get_mailchimp_member(asu_id)
        if member:
            return {"member":member},201
        else:
            return {"Not Found":
            "Student not signed up for mailchimp. Please sign up!:)"}, 404

    def _get_mailchimp_member(self,asu_id):
        """Check if asu student is part of soda mailchimp list"""
        return self.redis_service.redis_server.get(asu_id)
            

class GenerateAuthToken(Resource):
    """
    GenerateAuthToken endpoint creates a token if basic auth is accepted
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
        