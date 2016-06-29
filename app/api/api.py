from flask_restful import Resource, fields
from flask_restful import marshal_with, reqparse
from mailchimp import chimp
import json

list_info = {
    'list_id': fields.String,
    'list_name': fields.String
}

class MailChimpApi(Resource):
    """Rest API for parsing MailChimp Data"""
 
    def get(self,list_id):
        """A list of members from mailchimp"""
        args = self.parse_list_id().parse_args()
        
        r = chimp.ChimpRequester()
        
        return r.get_list(list_id,"test",json=True)
        
        
    def parse_list_id(self):
        lid_parser = reqparse.RequestParser()
        lid_parser.add_argument(
            'list_id', dest='list_id',
            type=str, help='ID of the mailchimp list',
        )
        return lid_parser
        
        
        
 
list_info = {
    'list_id': fields.String,
    'list_name': fields.String
}
# list_fields = {
#     'list_id': fields.String,
#     'list_name': fields.String,
#     'students' : fields.Nested(student_field)
# }   
   
# student_field = {
#     'first_name' :fields.String,
#     'last_name' : fields.String,
#     'email': fields.String,
#     'number': fields.String,
#     'asuid' : fields.String,
#     'class_standing': fields.String
# }