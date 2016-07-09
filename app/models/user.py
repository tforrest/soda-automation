from passlib.apps import custom_app_context as pwd_context
from config import db

class User(db.Model):
    """Basic user model for token creation"""
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(60), index=True)
    password = db.Column(db.String(60))
    # dont expose through the API!
    def hash_pass(self,pwd):
        """Hash Password to store"""
        self.password = pwd_context.encrypt(pwd)
    
    def check_pass(self,pwd):
        """Checks if the password is correct"""
        return pwd_context.verify(pwd, self.password)

    def __str__(self):
        return "User: %s".format(self.user_name)
