from requests.auth import HTTPBasicAuth
import requests
import os


class MailChimpBaseClass(object):
    """Base MailChimp Class for querying data"""
    
    def __init__(self,**kwargs):
        self._dc = "us13"
        self._api_version = "3.0"
        self._base_url = 'https://{}.api.mailchimp.com/{}/'.format(self._dc,self._api_version) 
        self._user_name = os.environ['MAILCHIMP_USER']
        self._api_key = os.environ['MAILCHIMP_AUTH']
        self._session = self._get_session(self._user_name,self._api_key)
  
     def _get_session(self,user,key):
         """Return mailchimp session"""
         s = requests.Session()
         s.auth(user,key)
         
         return s
        
    def _post_request(self,path):
        """Return response from POST request"""
        r = self._session.post(self._base_url+path)
        
        return r.json()
     
    def _get_request(self,path):
        """Return response from GET request"""
        r = self._session.get(self.base_url+path)
       
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