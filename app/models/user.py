from passlib.apps import custom_app_context as pwd_context
from config import db

class User(db.Model):
    """Basic user model for token creation"""
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(60), index=True)
    password = db.Column(db.String(60))
    def __init__(self,id,name,password):
        self.id = id
        self.user_name = user_name
        self.password = self._hash_pass(password)

    # dont expose through the API!
    def _hash_pass(self,pwd):
        """Hash Password to store"""
        self.password = pwd_context.encrypt(pwd)
    
    def check_pass(self,pwd):
        """Checks if the password is correct"""
        return pwd_context.verify(pwd, self.password)

    def __str__(self):
        return "User: %s".format(self.user_name)
