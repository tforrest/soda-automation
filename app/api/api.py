from flask_restful import Resource, fields
from flask_restful import marshal_with, reqparse
from mailchimp import chimp
import json

list_info = {
    'list_id': fields.String,
    'list_name': fields.String
}

student_field = {
    'first_name' :fields.String,
    'last_name' : fields.String,
    'email': fields.String,
    'number': fields.String,
    'asuid' : fields.String,
    'class_standing': fields.String
}

class MailChimpApi(Resource):
    """Rest API for parsing MailChimp Data"""
 
    def get(self,list_id):
        """A list of members from mailchimp"""
        args = self.parse_list_id().parse_args()
        r = chimp.ChimpRequester()
        return r.get_list(list_id,"test",json=True)
    @marshal_with(student_field)  
    def post(self,list_id):
        args = self.parse_list_id().parse_args()
        r = chimp.ChimpRequester()
        
        
        
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
            'first_name', dest='fiest_name',
            type=str, help='First name of student',
            required=True,
        )
        parser.add_argument(
            'last_name', dest='last_name',
            type=str, help='Last name of student',
            required=True,
        )
        parser.add_argument(
            'email', dest='email',
            type=str, help='Email of student',
        )
        parser.add_argument(
            'number', dest='number',
            type=str, help="Cell Number for student",
        )
        parser.add_argument(
            'asuid', dest='asuid',
            type=str, required=True,
            help='ASU id of student',
        )
        
        
        
 
list_info = {
    'list_id': fields.String,
    'list_name': fields.String
}
# list_fields = {
#     'list_id': fields.String,
#     'list_name': fields.String,
#     'students' : fields.Nested(student_field)
# }   
   