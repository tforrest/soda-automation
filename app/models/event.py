from config import db

# helper table for many-to-many relationship between students and events

# events = db.Table('events',
#             db.Column('event_id',db.Integer, db.ForeignKey('event.id')),
#             db.Column('student_id',db.Integer,db.ForeignKey('student.id'))
# )

# class Event(db.Model):
#     """Basic Model for events"""
#     id = db.Column(db.Integer, primary_key=True)
#     event_name = db.Column(db.String(50), nullable=False)
#     host_company = db.Column(db.String(50), nullable=True)
#     description = db.Column(db.String(100), nullable=False)
#     start_time = db.Column(db.DateTime, nullable=False)
#     end_time = db.Column(db.DateTime, nullable=False)
#     attendees = db.relationship('Student',secondary=events,backref=db.backref('events',lazy='dynamic'))
    
#     def __init__(self, id, event_name, host_company,description, start_time, end_time):
#         self.event_name = event_name
#         self.host_company = host_company
#         self.description = description
#         self.start_time = start_time
#         self.end_time = end_time
    
#     def __repr__(self):
#         return "Event: %s" % self.name
        
class Student(db.Model):
    """Basic Model for asu students"""
    # corresponds to mailchimp id 
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    asu_id = db.Column(db.String(20),nullable=False)
    class_standing = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    
    def __init__(self,first_name,last_name,asu_id,class_standing,email,phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.asu_id = asu_id
        self.class_standing = class_standing
        self.email = email
        self.phone_number = phone_number
        
    def __str__(self):
        return "ASU Student: %s %s".format(self.first_name, self.last_name)
   
    def __repr__(self):
    	return "ASU Student: %d, %s %s".format(self.asu_id, self.first_name, self.last_name)
