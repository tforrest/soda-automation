from flask_restful import Resource, fields
from flask_restful import reqparse
from flask import request
from util import validate_memmber
from util import resp_match

from mailchimp import chimp

requester = chimp.ChimpRequester()

class MailChimpListApi(Resource):
    """Rest API for parsing MailChimp List Data"""
    
    def __init__(self):
        super(Resource,self).__init__()
   
    def get(self,list_id):
        """A list of members from mailchimp"""
        r = requester.get_list(list_id,"test",json=True)
        if resp_match(str(r.status_code)):
            return r.json(),r.status_code
        resp = self._transform_mailchimp_response(r.json())
        return resp, r.status_code

    def post(self,list_id):
        """Add a member(s) to a list"""
        data = request.get_json()
        # check if valid request
        v = validate_memmber(data)
        if not v[0]:
            return v[1], 400
        result = requester.add_member(list_id,data)
        if not result:
            return "Error sending mailchimp request", 418
        return r.json(),r.status_code

    def _transform_mailchimp_response(self,json_response):
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

class CheckMailChimp(Resource):
    """Check if a student is in mailchimp"""

    def __init__(self):
        super(Resource,self).__init__()
    
    def get(self,asu_id):
        """GET to see if a member is part of soda"""
        if self._is_mailchimp_member(asu_id):
            pass
            # add member to event and incrememt attendence
        else:
            return {"Response":"Student not signed up for mailchimp"}, 404

    def _is_mailchimp_member(self,asu_id):
        """Check if asu student is part of soda mailchimp list"""

        # stub 
        return False
