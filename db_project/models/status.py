from db_project.db_setup import Base
from sqlalchemy import Column, Integer, String


class RegistrationStatus(Base):
    __tablename__ = 'statuses'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)