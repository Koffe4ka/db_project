from db_project.db_setup import Base
from sqlalchemy import Column, Integer, String


class RegistrationStatus(Base):
    __tablename__ = 'statuses'
    id = Column(Integer, primary_key=True) # 1-Registered; 2-Waiting; 3-Cancelled
    name = Column(String, nullable=False)
