from app import db

class Event(db.Modal):
    
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), nullable=False)
    host_company = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    
    
    def __init__(self, id, event_name, host_company,description, start_time, end_time):
        self.event_name = event_name
        self.host_company = host_company
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
    
    def __repr__(self):
        return "Event: %s" % self.name
    
        
        
    
    
    
    