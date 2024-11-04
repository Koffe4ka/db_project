from db_project.db_setup import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Registration(Base):
    __tablename__ = 'registrations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    status_id = Column(Integer,ForeignKey('statuses.id'), nullable=False)
    registration_date = Column(DateTime, nullable=False)

    user = relationship('User', back_populates='registrations')
    course = relationship('Course', back_populates='registrations')
    status = relationship('RegistrationStatus')