from flask_restful import Resource, fields
from flask_restful import reqparse
from flask import request
from util.util import validate_memmber
from util.util import bad_resp_match
from mailchimp import chimp
from redis_ops.init_redis import RedisService

requester = chimp.ChimpRequester()


class MailChimpList(Resource):
    
    """Rest API for parsing MailChimp List Data"""
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
    def __init__(self):
        super(Resource,self).__init__()
        self.redis_service = RedisService()
    
    def get(self,asu_id):
        """GET to see if a member is part of soda"""
        if self._is_mailchimp_member(asu_id):
            return {"Success":
            "Member signed up on mailchimp"},201
        else:
            return {"Not Found":
            "Student not signed up for mailchimp"}, 404

    def _is_mailchimp_member(self,asu_id):
        """Check if asu student is part of soda mailchimp list"""
        if self.redis_service.redis_server.get(asu_id):
            return True
        return False
