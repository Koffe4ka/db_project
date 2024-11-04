from db_project.db_setup import Base
from sqlalchemy import Column, Integer, ForeignKey, Table


history = Table(
    'attended_courses', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
)