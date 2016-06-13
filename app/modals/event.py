from app import db

Base = declarative_base()

class Event(Base):
    
    id = db.Column(db.Interger, primary_key=True)
    event_name = db.Column(db.String(50), unique=True)
    host_company = db.Column(db.String(50))
    description = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    
    
    def __init__(self, id, event_name, host_company,description, start_time, end_time):
        self.event_name = event_name
        self.host_company = host_company
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
    
    def __repr__(self):
        return "Event: %s" % self.name
    
        
        
    
    
    
    