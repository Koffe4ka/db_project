from db_project.db_setup import Base, session
from sqlalchemy import Column, Integer, String, select

class Level(Base):
    __tablename__ = 'levels'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rank = Column(Integer, nullable=False)