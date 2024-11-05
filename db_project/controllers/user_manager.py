import db_project.models as mod
import sqlalchemy
def authenticate_user(username, password):
    user = USER_DB.get(username)
    if user and user["password"] == password:
        return user
    return None

def register_user(username, name, password):
    user = mod.User
    if username in USER_DB:
        return False 
    USER_DB[username] = {"name": name, "password": password}
    return True

def logout_user()