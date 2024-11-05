from sqlalchemy.orm import Session
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

