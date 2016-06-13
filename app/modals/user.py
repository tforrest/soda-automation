from app import db

class Users(db.Model):
    __table__ = 'Users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    asu_id = db.Column(db.Integer,unique=True)
    class_standing = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    
    def __init__(self,name,asu_id,class_standing,email,phone_number):
        self.name = name
        self.asu_id = asu_id
        self.class_standing = class_standing
        self.email = email
        self.phone_number = phone_number
        
    def __repr__(self):
        return "User's name: %s" % self.name
    
    @validates('email')
    def validate_email(self,email):
        return email
      
    @validates('phone_number')
    def validate_phone_number(self,phone_number):
        return phone_number
    
    
    
    
    
    
    
    
    
    