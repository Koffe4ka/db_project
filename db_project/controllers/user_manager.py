from db_project.models import User
import db_project.db_setup as db
from sqlalchemy import select
from datetime import datetime

def login(username:str, password:str):
    """
    Returns User object if login successfull
    Returns False if user not found or password doesnt match
    """
    session = db.SessionLocal()
    qry = select(User).where(User.username == username)
    user = session.execute(qry).scalars().one_or_none()
    if user and user.password == password:
        user.login_date = datetime.now()
        user.logout_date = None
        user.is_loggedin = True
        session.commit()
        return user
    return False

def register(username:str, name:str, password:str):
    """
    Returns True if user was created
    Returns False if user already exists
    """
    session = db.SessionLocal()
    qry = select(User).where(User.username == username)
    user = session.execute(qry).scalars().one_or_none()
    if user is None:
        new_user = User(username, password, name)
        new_user.login_date = None
        new_user.logout_date = None
        new_user.is_loggedin = False
        session.add(new_user)
        session.commit()
        return True
    else:
        return False

def logout(username:str):
    """
    Returns True if logout successfull
    Returns False if user was not found or not logged in
    """
    session = db.SessionLocal()
    qry = select(User).where(User.username == username)
    user = session.execute(qry).scalars().one_or_none()
    if user and user.is_loggedin:
        user.logout_date = datetime.now()
        user.is_loggedin = False
        session.commit()
        return True
    return False