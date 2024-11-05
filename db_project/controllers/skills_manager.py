from sqlalchemy.orm import Session
from sqlalchemy import select
from db_project.models import Skill
from db_project.models import Level
from db_project.db_setup import session

def add_skill( user_id: int, name: str, description: str, level_id: int):
    """Add a new skill for a user."""
    skill = Skill(name=name, description=description, level_id=level_id, user_id=user_id)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill

def get_user_skills(user_id: int):
    """Retrieve all skills associated with a specific user."""
    return session.query(Skill).filter(Skill.user_id == user_id).all()

def update_skill(skill_id: int, user_id: int, name: str = None, description: str = None, level_id: int = None):
    """Modify skill details if it belongs to the user."""
    skill = session.query(Skill).filter(Skill.id == skill_id, Skill.user_id == user_id).first()
    if skill:
        if name:
            skill.name = name
        if description:
            skill.description = description
        if level_id is not None:
            skill.level_id = level_id
        session.commit()
        session.refresh(skill)
    return skill

def delete_skill(skill_id: int, user_id: int):
    """Remove a skill if it belongs to the user"""
    skill = session.query(Skill).filter(Skill.id == skill_id, Skill.user_id == user_id).first()
    if skill:
        session.delete(skill)
        session.commit()
    return skill

def get_levels():
    qry = select(Level).order_by(Level.rank)
    return session.execute(qry).scalars().all()

##########TEMP#############
lvls = [
    {'name':'Beginner', 'rank':1},
    {'name':'Intermediate', 'rank':2},
    {'name':'Advanced','rank':3},
    {'name':'Expert','rank':4}
]

for level in lvls:
    qry = select(Level).where(Level.rank == level['rank'])
    level_exists = session.execute(qry).scalars().one_or_none()
    if not level_exists:
        new_level = Level()
        new_level.name = level['name']
        new_level.rank = level['rank']
        session.add(new_level)
session.commit()
##########TEMP#############