from datetime import datetime
from db_project.models import Course, Registration
from db_project.db_setup import session
from sqlalchemy import select, or_, and_
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
    
def get_others_courses(user_id: int = None):
    qry = select(Course)
    return session.execute(qry).scalars().all()

def register_to_course(user_id:int, course_id:int):
    """
    Returns registration status
    0 - Nothing happened. Either course doesnt exists, or previous status did not change
    1 - Registration status changed to Registered
    2 - Registration status changed to Waiting
    """
    qry = select(Course).where(Course.id == course_id)
    course = session.execute(qry).scalars().one_or_none()

    if course:
        qry = select(Registration).where(Registration.course_id == course_id).order_by(Registration.registration_date)
        registrations = session.execute(qry).scalars().all()
        registered = [reg for reg in registrations if reg.status == 1]
        qry = qry.where(Registration.user_id == user_id).where(Registration.status_id == 2)
        existing_registration = session.execute(qry).scalars().one_or_none()
        if len(registered) < course.max_participants:
            if existing_registration:
                existing_registration.status_id = 1
            else:
                new_registration = Registration(user_id=user_id, course_id=course_id, status_id=1, registration_date=datetime.now())
                session.add(new_registration)
            session.commit()
            return 1

        if not existing_registration:
            new_registration = Registration(user_id=user_id, course_id=course_id, status_id=2, registration_date=datetime.now())
            session.add(new_registration)
            session.commit()
            return 2
    return 0

def cancel_registration(user_id:int, course_id:int):
    """
    Returns True if registreation was cancelled
    Returns False if registration does not exist or is already cancelled
    """

    qry = select(Registration).where(and_(Registration.user_id == user_id, Registration.course_id == course_id)).where(or_(Registration.status_id == 2, Registration.status_id == 1))
    existing_registration = session.execute(qry).scalars().one_or_none()
    if existing_registration:
        existing_registration.status_id = 3
        session.commit()
        register_waiting_list(course_id)
        return True
    return False
    
def register_waiting_list(course_id:int):
    """
    Returns number(int) of registrations converted from waiting to registered
    """

    qry = select(Registration).where(and_(Registration.course_id == course_id, Registration.status_id==2)).order_by(Registration.registration_date)
    waiting = session.execute(qry).scalars().all()
    result = 0
    if waiting:
        for reg in waiting: # loop through each waiting user and change from waiting to register if there are available spots
            if register_to_course(reg.user_id, course_id) == 1:
                result +=1
                continue
            break
    return result





def get_course_by_skill(skill_id: int):
    qry = select(Course).where(Course.skill_id == skill_id)
    return session.execute(qry).scalars().one_or_none()