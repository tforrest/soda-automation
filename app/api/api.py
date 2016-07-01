from flask_restful import Resource, fields
from flask_restful import marshal_with, reqparse
from flask import request, jsonify
from util import validate_memmber

from mailchimp import chimp


class MailChimpListApi(Resource):
    """Rest API for parsing MailChimp Data"""
    
    def __init__(self):
        self.requester = chimp.ChimpRequester()
        super(Resource,self).__init__()
   
    def get(self,list_id):
        """A list of members from mailchimp"""
        args = self.parse_list_id().parse_args()
        return self.requester.get_list(list_id,"test",json=True)
        

    def post(self,list_id):
        """Add a member to a list"""
        json_data = request.get_json()
        # check if valid request
        v = validate_memmber(json_data)
        
        if not v[0]:
            return v[1], 400
        try:
            pass
            # result = self.requester.add_member(list_id,json_data)
        except Exception as e:
            return e, 400
        return "",204
        
    def parse_list_id(self):
        lid_parser = reqparse.RequestParser()
        lid_parser.add_argument(
            'list_id', dest='list_id',
            type=str, help='ID of the mailchimp list',
        )
        return lid_parser
        