from passlib.apps import custom_app_context as pwd_context
from config import db

class User(db.Model):
    """Basic user model for token creation"""
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(60), index=True)
    password = db.Column(db.String(60))

    def __init__(self,user_name,password):
        self.user_name = user_name
        self.password = self._hash_pass(password)

    def _hash_pass(self,password):
        """Hash Password to store"""
        return pwd_context.encrypt(password,category='admin')
    
    def check_pass(self,pwd):
        """Checks if the password is correct"""
        return pwd_context.verify(pwd, self.password)

    def __str__(self):
        return "User: {}".format(self.user_name)
