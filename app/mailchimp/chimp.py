from requests.auth import HTTPBasicAuth
from util import handle_chimp_response
import requests
import json
import os

class ChimpRequester(object):
    """Base MailChimp Class for querying data"""
    
    def __init__(self,**kwargs):
        self._dc = "us13"
        self._api_version = "3.0"
        self._base_url = 'https://{}.api.mailchimp.com/{}/'.format(self._dc,self._api_version) 
        self._user_name = os.environ['MAILCHIMP_USER']
        self._api_key = os.environ['MAILCHIMP_AUTH']
        self._session = self._get_session(self._user_name,self._api_key)
  
    def _get_session(self,user,apikey):
         """Return mailchimp session"""
         s = requests.Session()
         s.auth = (user,apikey)
         return s
    
    @handle_chimp_response    
    def _post_request(self,path):
        """Return response from POST request"""
           
        r = self._session.post(self._base_url+path)
        
        return r
    
    @handle_chimp_response   
    def _get_request(self,path):
        """Return response from GET request"""
        
        r = self._session.get(self._base_url+path)
       
        return r
    
    @handle_chimp_response   
    def _patch_request(self,path):
        """Return response from PATCH request"""
        r = self._session.patch(self._base_url+path)
        
        return r
    
    @handle_chimp_response   
    def _put_request(self,path):
        """Return response from PUT request"""
        r = self._session.put(self._base_url+path)
        
        return r
    
    @handle_chimp_response   
    def _delete_request(self,path):
        """Return response from DELETE request"""
        r = self._session.delete(self._base_url+path)
        
        return r  

    def get_list(self,list_id,list_name,body=""):
        """"Return a list of people on  
            a mail chimp list 
        """
        path = "lists/{}/members".format(list_id)
        
        json_response = self._get_request(path)
        
        
        # Create a new list and filter out data not needed
        
        mail_chimp_list = ChimpList(list_name,list_id,json_response["members"])
       
        return mail_chimp_list
  
class ChimpList(object):
    """Object that holds a mail chimp with users"""
    
    def __init__(self,list_name,list_id,members):
        self.list_name = list_name 
        self.list_id = list_id
        self._members = self._process_members(members)
    
    def print_all(self):
        print "List Name:{}\nList ID:{}\nMembers:\n".format(self.list_name,self.list_id)
        for m in self._members:
            m.print_info()
 
    def _process_members(self,members):
       """Process the members into objects"""
       # list of members objects 
       p_m = []
       for m in members:
           p_m.append(self._process(m))
       return p_m
 
    def _process(self,member):
       """Process a single member"""
       
       # Pull out the desired attrbutes 
       data = dict()
       data["ID"] = member["id"]
       data["EMAIL"] = member["email_address"]
       
       # copy data in merge_fields
       temp = member["merge_fields"].copy()
       data.update(temp)
       
       # Create a member object 
       p_m = ChimpMember(data)
       
       return p_m
         
class ChimpMember(object):
    """Object holding a single members information"""
    
    def __init__(self,data):
        # TO-DO find better way to be explicit yet not use dicts
        # to not have key erros 
        self.id = data['ID']
        self.first_name = data['FNAME']
        self.last_name = data['LNAME']
        self.email = data['EMAIL']
        self.number = data['NUMBER']
        self.asuid = data['ASUID']
        self.class_standing = data['CLASS']

    def print_info(self):
        """"Print out memeber fields"""
        tmpl = ("First Name: {first_name}\n"
                "Last Name: {last_name}\n"
                "Email: {email}\n"
                "Phone number: {number}\n"
                "ASU ID: {asuid}\n"
                "Class Standing: {class_standing}\n")
        print tmpl.format(
            first_name=self.first_name, \
            last_name=self.last_name, \
            email=self.email, \
            number=self.number, \
            asuid=self.asuid,
            class_standing=self.class_standing)
    