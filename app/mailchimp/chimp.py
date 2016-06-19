from requests.auth import HTTPBasicAuth
from app import db
import requests
import json
import os


class MailChimpBaseWrapper(object):
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
         s.auth(user,apikey)
         return s
        
    def _post_request(self,path):
        """Return response from POST request"""
           
        r = self._session.post(self._base_url+path)
        
        return r.json()
     
    def _get_request(self,path,body):
        """Return response from GET request"""
        
        r = self._session.get(self._base_url+path,body)
       
        return r.json()
        
    def _patch_request(self,path):
        """Return response from PATCH request"""
        r = self._session.patch(self._base_url+path)
        
        return r.json()
        
    def _put_request(self,path):
        """Return response from PUT request"""
        r = self._session.put(self._base_url+path)
        
        return r.json()
    
    def _delete_request(self,path):
        """Return response from DELETE request"""
        r = self._session.delete(self._base_url+path)
        
        return r.json()
 
    def get_list(self,list_id,name,body=""):
        """"Return a list of people on  
            a mail chimp list 
        """"
        path = "lists/{}/members".format(list_id)
        
        json_response = self._get_request(path,body)
        
        l = json.loads(json_response)
        
        # Create a new list and filter out data not needed
        
        mail_chimp_list = MailChimpListBase(name,list_id,l)
       
        return mail_chimp_list
  
class MailChimpListBase(object):
    """Object that holds a mail chimp with users"""
    
    def __init__(self,list_name,members):
        self.list_name = list_name 
        self.list_id = list_id
        self.members = self._process_members(members)
 
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
       data["id"] = member["id"]
       data["email"] = member["email"]
       
       # copy data in merge_fields
       temp = member["merge_fields"].copy()
       data.update(temp)
       
       # Create a member object 
       p_m = MailChimpBaseMember(data)
       
       return p_m
         
class MailChimpBaseMember(object):
    """Object holding a single member's information"""
    
    def __init__(self,**kwargs):
        # Initalize any number of member attributes 
        for key, value in kwargs.iterm():
            setattr(self,key,value)