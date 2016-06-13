from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from sqlalchemy import Column, Integer, DateTime, String


Base = declarative_base()

class Users(Base):
    __table__ = 'Users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    asu_id =Column(Integer,nullable=False)
    class_standing = Column(String(100), nullable=True)
    email = Column(String(100))
    phone_number = Column(String(100))
    
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
    
    
    
    
    
    
    
    
    
    