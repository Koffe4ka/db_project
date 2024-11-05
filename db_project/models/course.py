from db_project.db_setup import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db_project.models.history import history


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    max_participants = Column(Integer, nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)

    user = relationship('User', back_populates='courses')
    attendees = relationship('User', secondary=history, back_populates='attended_courses')
    skill = relationship('Skill', back_populates='courses')
    registrations = relationship('Registration', back_populates='course')