from datetime import datetime

from altair import Description
from db_project.models import Course
from db_project.db_setup import session
from sqlalchemy import select
def add_course(name:str, description:str, start_date: datetime, end_date: datetime, max_participants: int, skill_id:int, user_id: int):
    """
    Returns True if course was added successfully
    Returns False if course for this skill already exists
    """
    new_course = Course(
        name = name,
        description = description,
        start_date = start_date,
        end_date = end_date,
        max_participants = max_participants,
        skill_id = skill_id,
        user_id = user_id
    )
    qry = select(Course).where(Course.skill_id == skill_id)
    course = session.execute(qry).scalars().one_or_none()
    if not course:
        session.add(new_course)
        session.commit()
        return True
    else:
        return False

def get_my_courses(user_id:int):
    qry = select(Course).where(Course.user_id == user_id)
    return session.execute(qry).scalars().all()
    
def get_others_courses(user_id:int):
    qry = select(Course).where(Course.user_id != user_id)
    return session.execute(qry).scalars().all()

def register_to_course(user_id:int, course_id:int):
    ...