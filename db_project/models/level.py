from db_project.db_setup import Base
from sqlalchemy import Column, Integer, String

class Level(Base):
    __tablename__ = 'levels'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)