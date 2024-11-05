from sqlalchemy.orm import Session
from models.skill import Skill
from models.level import Level

def add_skill(db: Session, user_id: int, name: str, description: str, level_id: int):
    """Add a new skill for a user."""
    skill = Skill(name=name, description=description, level_id=level_id, user_id=user_id)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill

def get_user_skills(db: Session, user_id: int):
    """Retrieve all skills associated with a specific user."""
    return db.query(Skill).filter(Skill.user_id == user_id).all()

def update_skill(db: Session, skill_id: int, user_id: int, name: str = None, description: str = None, level_id: int = None):
    """Modify skill details if it belongs to the user."""
    skill = db.query(Skill).filter(Skill.id == skill_id, Skill.user_id == user_id).first()
    if skill:
        if name:
            skill.name = name
        if description:
            skill.description = description
        if level_id is not None:
            skill.level_id = level_id
        db.commit()
        db.refresh(skill)
    return skill

def delete_skill(db: Session, skill_id: int, user_id: int):
    """Remove a skill if it belongs to the user"""
    skill = db.query(Skill).filter(Skill.id == skill_id, Skill.user_id == user_id).first()
    if skill:
        db.delete(skill)
        db.commit()
    return skill

