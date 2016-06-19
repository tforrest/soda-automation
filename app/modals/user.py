from config import db

class ASUStudent(db.Modal):
    """Basic Modal for asu students"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    asu_id = db.Column(db.Integer,nullable=False)
    class_standing = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    
    def __init__(self,name,asu_id,class_standing,email,phone_number):
        self.name = name
        self.asu_id = asu_id
        self.class_standing = class_standing
        self.email = email
        self.phone_number = phone_number
        
    def __repr__(self):
        return "ASU Student: %s %s".format(self.fist_name, self.last_name)