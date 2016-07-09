from flask_restful import Resource, fields
from flask_restful import reqparse
from flask import request

from util.danger import gen_auth_token
from util.danger import enable_auth
from util.util import validate_memmber
from util.util import bad_resp_match

from mailchimp import chimp

from models.user import User
from redis_ops.init_redis import RedisService

requester = chimp.ChimpRequester()


class MailChimpList(Resource):
    """Rest API for parsing MailChimp List Data"""
    method_decorators = [enable_auth]
    def __init__(self):
        super(Resource,self).__init__()

    def post(self,list_id):
        """Add a member(s) to a list"""
        data = request.get_json()
        # check if valid request
        v = validate_memmber(data)
        if not v[0]:
            return v[1], 400
        result = requester.add_member(list_id,data)
        if not result:
            return {"Errors" : {
                "MailChimp":"Failure to insert member",
            }}, 418
        return r.json(),r.status_code

class MailChimpMember(Resource):
    """Check if a student is in mailchimp"""
    method_decorators = [enable_auth]
    def __init__(self):
        super(Resource,self).__init__()
        self.redis_service = RedisService()

    def get(self,asu_id):
        """GET to see if a member is part of soda"""
        if self._is_mailchimp_member(asu_id):
            return {"Success":
            "Member signed up on mailchimp!Yay:)"},201
        else:
            return {"Not Found":
            "Student not signed up for mailchimp. Please sign up!:)"}, 404

    def _is_mailchimp_member(self,asu_id):
        """Check if asu student is part of soda mailchimp list"""
        if self.redis_service.redis_server.get(asu_id):
            return True
        return False

class GenerateAuthToken(Resource):
    """Resource to create auth token"""
    def get(self):
        """Return a valid token if basic_auth is successful"""
        auth = request.authorization
        if not auth:
            return {"Error":"Auth not found"}, 400
        if not self._check_basic_auth(auth):
            return {"Error": "Invalid Auth"}, 401

        token = gen_auth_token(auth.username)
        resp = {
            "Success!": "Token created",
            "token": token,
        }
        return resp,201

    def _check_basic_auth(self,auth):
        """Check if basic auth is correct"""
        u = auth.username
        p = auth.password
        if not u or not p:
            return False
        db_user = User.filter_by(user_name=u).first()
        if not db_user or not db_user.check_pass(p):
            return False
        return True 
        