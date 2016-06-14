from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String

Base = declarative_base()

class Event(Base):
    
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    event_name = Column(String(50), nullable=False)
    host_company = Column(String(50), nullable=True)
    description = Column(String(100), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    
    def __init__(self, id, event_name, host_company,description, start_time, end_time):
        self.event_name = event_name
        self.host_company = host_company
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
    
    def __repr__(self):
        return "Event: %s" % self.name
    
        
        
    
    
    
    