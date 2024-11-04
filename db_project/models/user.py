from db_project.db_setup import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from db_project.models.history import history

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    login_date = Column(DateTime)
    logout_date = Column(DateTime)
    is_loggedin = Column(Boolean)

    skills = relationship('Skill', back_populates='user')
    courses = relationship('Course', back_populates='user')
    attended_courses = relationship('Course', secondary=history, back_populates='attendees')
    registrations = relationship('Registration', back_populates='user')

    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name