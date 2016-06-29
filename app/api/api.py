from flask_restful import Resource, fields
from flask_restful import marshal_with, reqparse
from flask import request, jsonify
from mailchimp import chimp
import json

# list_info = {
#     'list_id': fields.String,
#     'list_name': fields.String
# }

# student_field = {
#     'first_name' :fields.String,
#     'last_name' : fields.String,
#     'email': fields.String,
#     'number': fields.String,
#     'asuid' : fields.String,
#     'class_standing': fields.String
# }

class MailChimpApi(Resource):
    """Rest API for parsing MailChimp Data"""
 
    def get(self,list_id):
        """A list of members from mailchimp"""
        args = self.parse_list_id().parse_args()
        r = chimp.ChimpRequester()
        return r.get_list(list_id,"test",json=True)
        
 
    def post(self,list_id):
        json_data = request.get_json()
        print json_data
        r = chimp.ChimpRequester()
        return r.add_member(list_id,json_data)
        
    def parse_list_id(self):
        lid_parser = reqparse.RequestParser()
        lid_parser.add_argument(
            'list_id', dest='list_id',
            type=str, help='ID of the mailchimp list',
        )
        return lid_parser
        
    def parse_incoming_student(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'first_name', dest='first_name',
             help='First name of student',
            required=True, location='application/json',
        )
        parser.add_argument(
            'last_name', dest='last_name',
            help='Last name of student',
            required=True,location='form',
        )
        parser.add_argument(
            'email', dest='email',
            help='Email of student', location='form',
        )
        parser.add_argument(
            'number', dest='number',
             help="Cell Number for student", location='form',
        )
        parser.add_argument(
            'asuid', dest='asuid',
            type=str, required=True,
            help='ASU id of student', location='form',
        )
        return parser
        
        
 
list_info = {
    'list_id': fields.String,
    'list_name': fields.String
}
# list_fields = {
#     'list_id': fields.String,
#     'list_name': fields.String,
#     'students' : fields.Nested(student_field)
# }   
   